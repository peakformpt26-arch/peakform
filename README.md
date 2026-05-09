# PeakForm

Landing page da plataforma portuguesa de CrossFit & Performance, servida via **Streamlit**.

---

## Estrutura do projeto

```
peakform-1/
├── app.py            # Ponto de entrada Streamlit
├── index.html        # Landing page completa (HTML/CSS/JS)
├── requirements.txt  # Dependências Python
└── README.md
```

### `app.py`
Configura o Streamlit (wide layout, sem chrome), lê `index.html` e renderiza-o dentro de um iframe sem bordas via `st.components.v1.html`. Toda a navegação, animações e o botão Hotmart funcionam normalmente dentro do iframe.

### `index.html`
Landing page single-page com as seguintes secções:

| Secção | ID | Conteúdo |
|---|---|---|
| Navbar | — | Logo, links de âncora, CTA |
| Hero | — | Headline, sub-headline, stats |
| Sobre | `#sobre` | Proposta de valor + 4 cards de pilares |
| Programas | `#programas` | Card destacado "First Pull-Up" (Hotmart) + card "Bar Muscle-Up" (em breve) |
| Planos | `#planos` | 3 planos de preço (À la carte / Active / Coach) |
| Coaches | `#atleta` | Palmarés + citação do coach |
| CTA Final | — | Call-to-action de fecho |
| Footer | — | Copyright |

**Tecnologias usadas no HTML:**
- Google Fonts — Barlow Condensed + Barlow
- Hotmart Checkout Widget
- IntersectionObserver para animações de scroll (`.reveal`)

---

## Instalar e correr localmente

```bash
# 1. Clonar / entrar na pasta
cd peakform-1

# 2. Criar ambiente virtual (opcional mas recomendado)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Arrancar a aplicação
streamlit run app.py
```

Abre automaticamente em `http://localhost:8501`.

---

## Deploy (Streamlit Community Cloud)

1. Faz push do repositório para GitHub.
2. Em [share.streamlit.io](https://share.streamlit.io) clica **New app**.
3. Seleciona o repositório, branch `main` e ficheiro `app.py`.
4. Clica **Deploy** — fica disponível num URL público em segundos.

---

## Pagamentos

O botão **"Comprar agora"** no card *First Pull-Up* aponta para:

```
https://pay.hotmart.com/C102172215W?checkoutMode=2
```

Para alterar o produto, substitui o ID `C102172215W` pelo ID do teu produto Hotmart em `index.html`.

---

## Personalização rápida

| O que alterar | Onde |
|---|---|
| Cores da marca | Variáveis CSS `:root` no topo de `index.html` |
| Preços / textos | Secções `#programas` e `#planos` em `index.html` |
| Link de compra Hotmart | Atributo `href` do `.hotmart-custom-btn` |
| Palmarés do coach | Secção `#atleta` em `index.html` |
| Altura do iframe | Parâmetro `height` em `app.py` |
