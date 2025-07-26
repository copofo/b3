import streamlit as st
import yfinance as yf
import pandas as pd

# Título da aplicação web
st.set_page_config(page_title="Buscador B3 Gratuito", layout="centered")
st.title("📈 Buscador de Indicadores da B3 (Gratuito)")
st.markdown("""
Esta aplicação busca informações e indicadores fundamentalistas básicos de ações da B3
usando dados do Yahoo Finance.
""")

# Campo de entrada para o ticker
# Predefine PETR4.SA para facilitar o primeiro teste do usuário
ticker_input = st.text_input(
    "Digite o Ticker da Ação (ex: PETR4.SA, VALE3.SA):",
    value="PETR4.SA"
).upper() # Converte para maiúsculas automaticamente

# Botão para buscar os indicadores
if st.button("🔍 Buscar Indicadores"):
    if ticker_input:
        with st.spinner(f"Buscando dados para {ticker_input}..."):
            try:
                # Baixa as informações do ticker usando yfinance
                ticker = yf.Ticker(ticker_input)
                info = ticker.info # Dicionário com várias informações

                st.success(f"Dados encontrados para {ticker_input}!")
                st.subheader(f"📊 {info.get('longName', ticker_input)}") # Nome completo da empresa

                st.markdown("---") # Linha separadora

                # --- Principais Indicadores Fundamentalistas ---
                st.markdown("### Principais Indicadores Fundamentalistas:")

                # Função auxiliar para exibir indicadores
                def display_indicator(label, value, format_str=None, default_text="N/D"):
                    if value is not None:
                        if format_str:
                            st.write(f"- **{label}:** {format_str.format(value)}")
                        else:
                            st.write(f"- **{label}:** {value}")
                    else:
                        st.write(f"- **{label}:** {default_text}")

                # Preço/Lucro (P/L)
                pe_ratio = info.get('forwardPE')
                if pe_ratio is None:
                    pe_ratio = info.get('trailingPE')
                display_indicator("P/L (Preço/Lucro)", pe_ratio, "{:.2f}")

                # Preço/Valor Patrimonial (P/VP)
                pb_ratio = info.get('priceToBook')
                display_indicator("P/VP (Preço/Valor Patrimonial)", pb_ratio, "{:.2f}")

                # Retorno sobre o Patrimônio Líquido (ROE)
                roe = info.get('returnOnEquity')
                display_indicator("ROE (Retorno sobre o PL)", roe, "{:.2%}") # Formato percentual

                # Dividend Yield
                dividend_yield = info.get('dividendYield')
                display_indicator("Dividend Yield", dividend_yield, "{:.2%}")

                # Margem Líquida
                profit_margins = info.get('profitMargins')
                display_indicator("Margem Líquida", profit_margins, "{:.2%}")

                # --- Outras Informações da Empresa ---
                st.markdown("---")
                st.markdown("### Outras Informações:")

                # Setor e Indústria
                sector = info.get('sector')
                industry = info.get('industry')
                if sector and industry:
                    st.write(f"- **Setor/Indústria:** {sector} / {industry}")
                elif sector:
                    st.write(f"- **Setor:** {sector}")
                else:
                    st.write("- **Setor/Indústria:** N/D")

                # Capitalização de Mercado
                market_cap = info.get('marketCap')
                if market_cap:
                    st.write(f"- **Capitalização de Mercado:** R$ {market_cap:,.2f}")
                else:
                    st.write("- **Capitalização de Mercado:** N/D")

                # Cotação Atual
                current_price = info.get('currentPrice')
                if current_price:
                    st.write(f"- **Preço Atual:** R$ {current_price:.2f}")
                else:
                    st.write("- **Preço Atual:** N/D")

                # --- Histórico de Preços (Gráfico e Tabela) ---
                st.markdown("---")
                st.markdown("### Histórico de Preços (Últimos 6 meses):")
                hist = ticker.history(period="6mo") # Pega os últimos 6 meses
                if not hist.empty:
                    # Gráfico interativo com Plotly (Streamlit usa por padrão)
                    st.line_chart(hist['Close'])
                    st.markdown("#### Últimos Preços de Fechamento:")
                    st.dataframe(hist[['Open', 'High', 'Low', 'Close', 'Volume']].tail(10)) # Mostra as últimas 10 linhas
                else:
                    st.write("Histórico de preços não disponível.")


            except Exception as e:
                # Mensagem de erro mais detalhada e amigável
                st.error(f"""
                **Erro ao buscar informações para '{ticker_input}'.**
                Por favor, verifique se:
                1. O ticker está correto (ex: `PETR4.SA`, `VALE3.SA`). Lembre-se do `.SA` para ações da B3.
                2. Sua conexão com a internet está funcionando.
                3. O Yahoo Finance tem dados disponíveis para este ticker.
                """)
                st.error(f"Detalhes técnicos do erro: {e}")
    else:
        st.warning("Por favor, digite um ticker para buscar os indicadores.")

# Sidebar com exemplos de tickers
st.sidebar.markdown("### Exemplos de Tickers da B3:")
st.sidebar.write("- `PETR4.SA` (Petrobras)")
st.sidebar.write("- `VALE3.SA` (Vale)")
st.sidebar.write("- `ITUB4.SA` (Itaú Unibanco)")
st.sidebar.write("- `BBDC4.SA` (Bradesco)")
st.sidebar.write("- `WEGE3.SA` (Weg)")
st.sidebar.write("- `MGLU3.SA` (Magazine Luiza)")
st.sidebar.markdown("---")
st.sidebar.info("Lembre-se sempre do `.SA` para ações da B3!")

st.markdown("---")
st.caption("Dados fornecidos por Yahoo Finance. Para fins educacionais e de aprendizado.")
