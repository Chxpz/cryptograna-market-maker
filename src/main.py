"""
Orquestrador principal do bot de market making.
"""
import os
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv

from collector.market_data_collector import MarketDataCollector
from ai_engine.market_maker import MarketMakerAI
from hb_controller import HummingbotController

# Configuração
load_dotenv()
logger = logging.getLogger(__name__)

class MarketMakingBot:
    def __init__(self):
        # Inicializa componentes
        self.collector = MarketDataCollector()
        self.ai = MarketMakerAI(self.collector)
        self.hb_controller = HummingbotController()
        
        # Configuração
        self.update_interval = int(os.getenv("UPDATE_INTERVAL", "30"))
        self.is_running = False
        
    async def start(self):
        """Inicia o bot."""
        self.is_running = True
        logger.info("Iniciando bot de market making")
        
        # Inicia controlador do Hummingbot
        asyncio.create_task(self.hb_controller.start())
        
        while self.is_running:
            try:
                # Coleta dados de mercado
                market_data = await self.collector.collect_market_data()
                logger.info(f"Dados de mercado coletados: {market_data}")
                
                # Gera recomendações via IA
                recommendations = await self.ai.get_recommendations(market_data)
                logger.info(f"Recomendações geradas: {recommendations}")
                
                # Atualiza parâmetros no Hummingbot
                await self.hb_controller.update_parameters(recommendations)
                
                # Aguarda próximo ciclo
                await asyncio.sleep(self.update_interval)
                
            except Exception as e:
                logger.error(f"Erro no bot: {e}")
                await asyncio.sleep(5)  # Espera antes de tentar novamente
    
    async def stop(self):
        """Para o bot."""
        self.is_running = False
        await self.hb_controller.stop()
        logger.info("Bot parado")

async def main():
    """Função principal."""
    # Configura logging
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Inicia bot
    bot = MarketMakingBot()
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Interrompendo bot...")
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main()) 