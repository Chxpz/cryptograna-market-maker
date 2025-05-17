# Solana Market Making Bot

A high-performance market making bot for Solana DEXes, built with Python and Hummingbot.

## Features

### Core Components
- **Market Data Collector**: Real-time data collection from multiple sources with validation and rate limiting
- **Trading Strategy**: Pure market making with dynamic parameter adjustment
- **Hummingbot Controller**: Order execution and parameter management
- **Monitoring System**: Prometheus metrics and Grafana dashboards

### Key Features
- Real-time market data collection from Helius, Jupiter, and Orca
- Dynamic spread and order size calculation
- Position tracking and risk management
- Circuit breakers for drawdown protection
- Comprehensive monitoring and metrics
- Automated error recovery
- Rate limiting and caching

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Hummingbot instance
- API keys for:
  - Helius
  - Jupiter
  - Orca

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/solana-market-making-bot.git
cd solana-market-making-bot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file and configure it:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

The bot is configured through environment variables. Key settings include:

### API Keys
- `HELIUS_API_KEY`: Your Helius API key
- `JUPITER_API_KEY`: Your Jupiter API key
- `ORCA_API_KEY`: Your Orca API key

### Trading Parameters
- `MIN_SPREAD`: Minimum spread percentage
- `MAX_SPREAD`: Maximum spread percentage
- `ORDER_SIZE`: Base order size
- `MAX_POSITION_SIZE`: Maximum position size
- `UPDATE_INTERVAL`: Strategy update interval in seconds

### Risk Parameters
- `MAX_DRAWDOWN`: Maximum allowed drawdown
- `STOP_LOSS`: Stop loss percentage
- `MAX_LEVERAGE`: Maximum leverage

### Monitoring
- `PROMETHEUS_PORT`: Port for Prometheus metrics
- `METRICS_UPDATE_INTERVAL`: Metrics update interval
- `LOG_LEVEL`: Logging level

## Usage

1. Start the bot:
```bash
./scripts/run_bot.sh
```

2. Monitor performance:
- View logs in the `logs/` directory
- Access Grafana dashboard at http://localhost:3000
- View Prometheus metrics at http://localhost:9090

## Monitoring

The bot provides comprehensive monitoring through:

### Metrics
- Order metrics (placed, filled, cancelled)
- Position metrics (size, value, PnL)
- Market metrics (spread, volatility, liquidity)
- API latency
- Error counts

### Health Checks
- Component health status
- API connectivity
- Data validation
- Error tracking

### Alerts
- Circuit breaker triggers
- Error thresholds
- Performance degradation
- API issues

## Error Recovery

The bot implements automatic error recovery for:
- API connection issues
- Data validation failures
- Parameter calculation errors
- Order execution failures

## Development

### Project Structure
```
.
├── src/
│   ├── collector/         # Market data collection
│   ├── decision/          # Trading strategy
│   ├── monitoring/        # Metrics and monitoring
│   └── main.py           # Main trading loop
├── tests/                # Test suite
├── scripts/              # Utility scripts
└── docker/              # Docker configuration
```

### Running Tests
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hummingbot for the trading infrastructure
- Helius, Jupiter, and Orca for market data
- Prometheus and Grafana for monitoring

# Cryptograna Market Maker's Dashboard

## Visão Geral

O Cryptograna é um sistema de market making e gestão de portfólio para criptoativos, projetado para operar de forma **totalmente autônoma** ou com **supervisão/intervenção manual opcional**. O objetivo é maximizar o lucro e a eficiência operacional, minimizando a necessidade de intervenção humana.

### Modos de Operação

#### 1. Modo 100% Autônomo
- O sistema gerencia um **portfólio único de recursos** (master portfolio).
- Aloca recursos dinamicamente entre múltiplos bots, cada um operando pares e estratégias distintas.
- Identifica oportunidades, escolhe ativos, ajusta parâmetros do Hummingbot e executa operações visando o maior lucro possível.
- Lucros obtidos por cada bot são automaticamente repassados para a conta principal (master), de onde podem ser sacados.
- **Nenhuma intervenção manual é necessária**: o sistema aprende, executa, realoca e reporta tudo sozinho.

#### 2. Supervisão e Intervenção Manual Opcional
- O portfólio único e a lógica de repasses são mantidos.
- O usuário pode, a qualquer momento, criar manualmente um novo bot para operar um par específico em uma DEX, informando:
  - O endereço do pool correspondente aos ativos.
  - Parâmetros não-decisórios (ex: limites, frequência de atualização, etc).
- O racional de operação (estratégia, ajustes, decisões) continua sendo do sistema.
- O usuário tem **visão clara** do portfólio, dos bots ativos, dos lucros e pode acompanhar ou intervir na criação de bots.

### Diferenciais
- **Gestão centralizada de recursos**: todos os bots operam a partir de um portfólio master, com alocação dinâmica.
- **Repasses automáticos de lucro**: bots transferem ganhos para a conta principal.
- **Criação manual de bots**: flexibilidade para o usuário explorar pares/DEXes de interesse.
- **Transparência e controle**: dashboards detalhados, logs, e visão clara do que está acontecendo.

## Arquitetura
- **Portfolio Master**: controla saldo, alocação, repasses e saque.
- **Bots**: instâncias independentes, cada uma com sua configuração e recursos alocados.
- **Módulo de Decisão**: IA/algoritmo que escolhe ativos, ajusta parâmetros e realoca recursos.
- **Interface de Usuário**: dashboard para acompanhamento, criação de bots e visão do portfólio.

## Exemplos de Uso
- Deixar o sistema rodando 100% sozinho, apenas sacando lucros periodicamente.
- Criar manualmente um bot para um novo par promissor, alocando parte do portfólio master.
- Acompanhar a performance de cada bot e do portfólio geral em tempo real.
