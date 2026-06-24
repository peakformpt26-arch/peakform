// Supabase Edge Function: stripe-webhook
// Recebe eventos do Stripe e, ao concluir um pagamento, ativa o programa
// na conta do utilizador (tabela user_programs).
//
// Secrets necessários (Supabase → Edge Functions → Secrets):
//   STRIPE_SECRET_KEY        (sk_live_... ou sk_test_...)
//   STRIPE_WEBHOOK_SECRET    (whsec_... do endpoint do webhook)
// SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY são injetados automaticamente.

import Stripe from "https://esm.sh/stripe@14?target=deno";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY")!, {
  apiVersion: "2024-06-20",
  httpClient: Stripe.createFetchHttpClient(),
});
const webhookSecret = Deno.env.get("STRIPE_WEBHOOK_SECRET")!;

const supabase = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
);

Deno.serve(async (req) => {
  const signature = req.headers.get("stripe-signature");
  const body = await req.text();

  let event;
  try {
    event = await stripe.webhooks.constructEventAsync(body, signature!, webhookSecret);
  } catch (err) {
    console.error("Assinatura inválida:", err.message);
    return new Response("Invalid signature", { status: 400 });
  }

  if (event.type === "checkout.session.completed") {
    const session = event.data.object as any;
    const ref = (session.client_reference_id || "") as string;
    const [userId, programSlug] = ref.split("__");

    if (!userId || !programSlug) {
      console.warn("client_reference_id em falta ou mal formado:", ref);
      return new Response("ok", { status: 200 });
    }

    // Já tem o programa? (evita duplicados)
    const { data: existing } = await supabase
      .from("user_programs")
      .select("id")
      .eq("user_id", userId)
      .eq("program_slug", programSlug)
      .maybeSingle();

    if (!existing) {
      const { error } = await supabase
        .from("user_programs")
        .insert({ user_id: userId, program_slug: programSlug });
      if (error) {
        console.error("Falha ao ativar programa:", error.message);
        return new Response("db error", { status: 500 });
      }
      console.log(`Programa ${programSlug} ativado para ${userId}`);
    }
  }

  return new Response("ok", { status: 200 });
});
