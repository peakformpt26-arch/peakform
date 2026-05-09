# PeakForm

Plataforma portuguesa de CrossFit & Performance. Landing pública + área privada do atleta com programas de treino.

---

## Estrutura

```
peakform-1/
├── app.py                      # Entrada Streamlit — router de páginas
├── index.html                  # Landing page pública
├── input/
│   ├── PeakForm Icon.png           # Favicon
├── requirements.txt
├── README.md
└── input/
    ├── PeakForm Icon.png           # Favicon
    └── first-pullup-peakform.html  # Programa First Pull-Up
```

---

## Páginas / estados

| Estado | O que mostra |
|---|---|
| `landing` | Landing page pública (`index.html` em iframe) |
| `login` | Formulário de autenticação |
| `area_atleta` | Dashboard privado com card do programa |
| `first_pullup` | Programa completo (`first-pullup-peakform.html` em iframe) |

O router usa `st.session_state.page`. A navegação entre páginas nativas (login → área → programa) usa `st.button` para preservar a sessão. A navegação a partir do iframe da landing usa `window.parent.location.href='/?nav=X'`.

---

## Correr localmente

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Iniciar
streamlit run app.py
```

Abre em `http://localhost:8501`.

---

## Login de teste

> ⚠️ Autenticação fake — apenas para protótipo.

| Campo | Valor |
|---|---|
| Utilizador | `PeakFormTeste` |
| Palavra-passe | `teste123` |

---

## Fluxo completo de teste

1. Abrir `http://localhost:8501` → ver landing
2. Clicar **Login** (navbar ou botões da landing)
3. Inserir credenciais de teste → **Entrar**
4. Ver **Área do Atleta** com card First Pull-Up
5. Clicar **Abrir programa** → ver programa completo
6. Clicar **← Voltar à Área do Atleta**
7. Clicar **Sair** → voltar à landing sem sessão

---

## Programa First Pull-Up

O ficheiro está em:

```
peakform-1/input/first-pullup-peakform.html
```

A app detecta automaticamente o ficheiro. Se não existir, mostra uma mensagem de aviso na página do programa.

---

## Notas técnicas

- **HTTP interno**: `app.py` inicia um servidor HTTP Python na porta `8502` em background para servir os ficheiros HTML. Isto permite que os iframes carreguem scripts, fontes e vídeos Vimeo sem restrições de CORS.
- **Hotmart removido**: todos os scripts, CSS e links Hotmart foram removidos do `index.html`.
- **Autenticação**: fake, baseada em `st.session_state`. Não usar em produção sem autenticação real.

---

## Deploy (Streamlit Cloud)

1. Push do repositório para GitHub
2. [share.streamlit.io](https://share.streamlit.io) → New app → selecionar repo + `app.py`
3. Deploy

> **Nota**: no Streamlit Cloud, o servidor HTTP interno (porta 8502) não é acessível externamente — os iframes carregam os ficheiros via `localhost` dentro do mesmo container, pelo que o comportamento é idêntico ao local.
