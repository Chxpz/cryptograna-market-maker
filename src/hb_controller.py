"""
Controlador para o Hummingbot que atualiza parâmetros e monitora execução.
"""
import os
import yaml
import logging
import asyncio
from typing import Dict, Optional
from datetime import datetime
import aiohttp
from dotenv import load_dotenv

# Configuração
load_dotenv()
logger = logging.getLogger(__name__)

class HummingbotController:
    def __init__(self):
        self.config_path = os.getenv("HUMMINGBOT_CONFIG_PATH", "/app/hummingbot/conf")
        self.strategy = os.getenv("HUMMINGBOT_STRATEGY", "pure_market_making")
        self.update_interval = int(os.getenv("HUMMINGBOT_UPDATE_INTERVAL", "30"))
        
        # Configuração do Hummingbot
        self.config_file = f"{self.config_path}/conf_{self.strategy}_strategy.yml"
        
        # Estado atual
        self.current_params = {}
        self.last_update = None
        self.is_running = False
        
    async def start(self):
        """Inicia o controlador e monitora execução."""
        self.is_running = True
        logger.info("Iniciando controlador do Hummingbot")
        
        while self.is_running:
            try:
                # Verifica status do Hummingbot
                status = await self._check_status()
                
                if not status.get("is_running", False):
                    logger.warning("Hummingbot não está rodando, tentando reiniciar...")
                    await self._restart_hummingbot()
                
                # Aguarda próximo ciclo
                await asyncio.sleep(self.update_interval)
                
            except Exception as e:
                logger.error(f"Erro no controlador: {e}")
                await asyncio.sleep(5)  # Espera antes de tentar novamente
    
    async def update_parameters(self, params: Dict):
        """
        Atualiza parâmetros da estratégia no Hummingbot.
        
        Args:
            params: Dicionário com novos parâmetros
                - bid_spread: Spread para ordens de compra
                - ask_spread: Spread para ordens de venda
                - order_amount: Tamanho da ordem
                - inventory_target_base_pct: % alvo de inventory
        """
        try:
            # Carrega configuração atual
            current_config = self._load_config()
            
            # Atualiza parâmetros
            current_config["bid_spread"] = params["bid_spread"]
            current_config["ask_spread"] = params["ask_spread"]
            current_config["order_amount"] = params["order_amount"]
            current_config["inventory_target_base_pct"] = params["inventory_target_base_pct"]
            
            # Salva nova configuração
            self._save_config(current_config)
            
            # Atualiza estado
            self.current_params = params
            self.last_update = datetime.now()
            
            logger.info(f"Parâmetros atualizados: {params}")
            
            # Aplica nova configuração no Hummingbot
            await self._apply_config()
            
        except Exception as e:
            logger.error(f"Erro ao atualizar parâmetros: {e}")
            raise
    
    def _load_config(self) -> Dict:
        """Carrega configuração atual do arquivo YAML."""
        try:
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            return {}
    
    def _save_config(self, config: Dict):
        """Salva configuração no arquivo YAML."""
        try:
            with open(self.config_file, 'w') as f:
                yaml.dump(config, f)
        except Exception as e:
            logger.error(f"Erro ao salvar configuração: {e}")
            raise
    
    async def _apply_config(self):
        """Aplica nova configuração no Hummingbot via API."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://hummingbot:9000/command",
                    json={"command": "import_config_file", "file": self.config_file}
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Erro ao aplicar configuração: {response.status}")
                    
                    # Reinicia estratégia
                    await session.post(
                        "http://hummingbot:9000/command",
                        json={"command": "stop_strategy", "strategy": self.strategy}
                    )
                    await asyncio.sleep(1)
                    await session.post(
                        "http://hummingbot:9000/command",
                        json={"command": "start_strategy", "strategy": self.strategy}
                    )
                    
        except Exception as e:
            logger.error(f"Erro ao aplicar configuração: {e}")
            raise
    
    async def _check_status(self) -> Dict:
        """Verifica status do Hummingbot via API."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://hummingbot:9000/status") as response:
                    if response.status == 200:
                        return await response.json()
                    return {"is_running": False}
        except Exception as e:
            logger.error(f"Erro ao verificar status: {e}")
            return {"is_running": False}
    
    async def _restart_hummingbot(self):
        """Tenta reiniciar o Hummingbot."""
        try:
            async with aiohttp.ClientSession() as session:
                # Para todas as estratégias
                await session.post(
                    "http://hummingbot:9000/command",
                    json={"command": "stop_all"}
                )
                await asyncio.sleep(2)
                
                # Inicia estratégia
                await session.post(
                    "http://hummingbot:9000/command",
                    json={"command": "start_strategy", "strategy": self.strategy}
                )
                
                logger.info("Hummingbot reiniciado com sucesso")
                
        except Exception as e:
            logger.error(f"Erro ao reiniciar Hummingbot: {e}")
    
    async def stop(self):
        """Para o controlador."""
        self.is_running = False
        logger.info("Controlador do Hummingbot parado") 