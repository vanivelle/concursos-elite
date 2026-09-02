"""
🔒 MÓDULO AVANÇADO DE BLOQUEIOS DE SEGURANÇA
Detecta e bloqueia:
  • IPv6
  • Máquinas virtuais (PC/Celular)
  • VPN/Tor
  • GPU Cloud (AWS, Azure, GCP, etc)
"""

import socket
import re
import logging
from typing import Dict, Tuple
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DetectorSegurancaAvancada:
    """Detector de acessos suspeitos e bloqueáveis"""

    # Fingerprints conhecidas de VPN/Proxy
    VPN_PROVIDERS = {
        "nordvpn": ["nordvpn", "nord", "2.vpn"],
        "expressvpn": ["expressvpn", "express", "expressvpn.com"],
        "surfshark": ["surfshark", "surfshark.com"],
        "mullvad": ["mullvad", "mullvad.net"],
        "protonvpn": ["proton", "protonvpn"],
        "cyberghost": ["cyberghost", "cyber"],
        "windscribe": ["windscribe"],
        "hotspot": ["hotspotshield"],
        "ipvanish": ["ipvanish"],
        "privateinternet": ["privateinternetaccess", "pia"],
        "tor": ["tor", "torproject", ".onion"],
    }

    # IPs conhecidas de Tor exit nodes (sample)
    TOR_EXIT_NODES = {
        "109.105": "Tor network",
        "185.112": "Tor network",
        "198.50": "Tor network",
        "199.249": "Tor network",
        "62.102": "Tor network",
    }

    # Fingerprints de GPU Cloud
    GPU_CLOUD_PROVIDERS = {
        "aws": {
            "hostnames": ["ec2", "compute.amazonaws.com", "amazonaws"],
            "ip_ranges": ["52.", "54.", "35.", "50.", "176."]
        },
        "azure": {
            "hostnames": ["azure", "cloudapp.azure.com", "azurecontainer"],
            "ip_ranges": ["13.", "52.", "40.", "104.", "204."]
        },
        "gcp": {
            "hostnames": ["compute", "gstatic.com", "google", "googleusercontent"],
            "ip_ranges": ["34.", "35.", "104.", "107.", "130."]
        },
        "linode": {
            "hostnames": ["linode", "akamai"],
            "ip_ranges": ["45.", "139.", "172."]
        },
        "digitalocean": {
            "hostnames": ["digitalocean", "do.co"],
            "ip_ranges": ["104.", "159.", "167."]
        },
        "heroku": {
            "hostnames": ["heroku", "herokuapp"],
            "ip_ranges": ["50.", "54."]
        },
        "vultr": {
            "hostnames": ["vultr"],
            "ip_ranges": ["45.", "103.", "104."]
        },
        "kaggle": {
            "hostnames": ["kaggle", "colab"],
            "ip_ranges": ["34.", "35."]  # Google infraestrutura
        },
    }

    # VM Fingerprints (User-Agents, detecção de recursos)
    VM_FINGERPRINTS = {
        "user_agents": [
            "virtualbox", "vmware", "parallels", "qemu", "xen",
            "hyper-v", "hyperv", "vagrant", "docker",
            "proxmox", "kvm", "simulator", "emulator"
        ],
        "hostnames": [
            "virtualbox", "vmware", "qemu", "vagrant-", "docker",
            "hyperv", "parallels", "xen", "kvm", "simulator"
        ]
    }

    @staticmethod
    def verificar_ipv6(ip: str) -> Tuple[bool, str]:
        """
        Verifica se é IPv6
        
        Args:
            ip: String de IP
            
        Returns:
            (é_ipv6, mensagem)
        """
        try:
            socket.inet_pton(socket.AF_INET6, ip)
            return True, f"🚫 IPv6 detectado: {ip} - BLOQUEADO"
        except (socket.error, ValueError):
            # Nem é IPv6, continua
            if ":" in ip and ip.count(":") > 1:
                return True, f"🚫 IPv6 detectado: {ip} - BLOQUEADO"
            return False, "✅ IPv4 aceito"

    @staticmethod
    def verificar_vpn_tor(ip: str, hostname: str = "") -> Tuple[bool, str]:
        """
        Verifica se é VPN ou Tor
        
        Args:
            ip: String de IP
            hostname: Hostname/reverse DNS
            
        Returns:
            (é_vpn, mensagem)
        """
        hostname_lower = hostname.lower() if hostname else ""
        ip_lower = ip.lower()

        # Verificar Tor exit nodes
        for tor_prefix, tor_provider in DetectorSegurancaAvancada.TOR_EXIT_NODES.items():
            if ip.startswith(tor_prefix):
                return True, f"🚫 Tor network detectado ({ip}) - BLOQUEADO"

        # Verificar VPN providers
        for vpn_name, patterns in DetectorSegurancaAvancada.VPN_PROVIDERS.items():
            for pattern in patterns:
                if pattern in hostname_lower or pattern in ip_lower:
                    return True, f"🚫 VPN detectada ({vpn_name}: {ip}) - BLOQUEADO"

        # Verificar suspicious patterns
        if "proxy" in hostname_lower or "vpn" in hostname_lower:
            return True, f"🚫 Proxy/VPN suspeita detectada ({hostname}) - BLOQUEADO"

        return False, "✅ IP verificado (não-VPN)"

    @staticmethod
    def verificar_vm(user_agent: str = "", hostname: str = "") -> Tuple[bool, str]:
        """
        Verifica se é máquina virtual
        
        Args:
            user_agent: User-Agent do navegador
            hostname: Hostname do dispositivo
            
        Returns:
            (é_vm, mensagem)
        """
        user_agent_lower = user_agent.lower() if user_agent else ""
        hostname_lower = hostname.lower() if hostname else ""

        # Verificar User-Agents suspeitos
        for vm_indicator in DetectorSegurancaAvancada.VM_FINGERPRINTS["user_agents"]:
            if vm_indicator in user_agent_lower:
                return True, f"🚫 VM detectada (User-Agent: {vm_indicator}) - BLOQUEADO"

        # Verificar Hostnames
        for vm_indicator in DetectorSegurancaAvancada.VM_FINGERPRINTS["hostnames"]:
            if vm_indicator in hostname_lower:
                return True, f"🚫 VM detectada (Hostname: {vm_indicator}) - BLOQUEADO"

        return False, "✅ Dispositivo real verificado"

    @staticmethod
    def verificar_gpu_cloud(ip: str, hostname: str = "") -> Tuple[bool, str]:
        """
        Verifica se é GPU Cloud (AWS, Azure, GCP, etc)
        
        Args:
            ip: String de IP
            hostname: Hostname/reverse DNS
            
        Returns:
            (é_gpu_cloud, mensagem)
        """
        hostname_lower = hostname.lower() if hostname else ""

        for provider, config in DetectorSegurancaAvancada.GPU_CLOUD_PROVIDERS.items():
            # Verificar por hostname
            for pattern in config["hostnames"]:
                if pattern in hostname_lower:
                    return True, f"🚫 GPU Cloud detectada ({provider.upper()}: {hostname}) - BLOQUEADO"

            # Verificar por IP ranges
            for ip_range in config["ip_ranges"]:
                if ip.startswith(ip_range):
                    return True, f"🚫 GPU Cloud detectada ({provider.upper()}: {ip}) - BLOQUEADO"

        return False, "✅ Datacenter verificado (não-cloud)"

    @staticmethod
    def verificacao_completa(ip: str, user_agent: str = "", hostname: str = "") -> Dict:
        """
        Executa verificação completa de segurança
        
        Args:
            ip: IP do cliente
            user_agent: User-Agent do navegador
            hostname: Hostname/reverse DNS
            
        Returns:
            Dict com resultado de todas as verificações
        """
        resultado = {
            "timestamp": datetime.now().isoformat(),
            "ip": ip,
            "bloqueado": False,
            "razoes": [],
            "detalhes": {}
        }

        # 1. Verificar IPv6
        eh_ipv6, msg_ipv6 = DetectorSegurancaAvancada.verificar_ipv6(ip)
        resultado["detalhes"]["ipv6"] = msg_ipv6
        if eh_ipv6:
            resultado["bloqueado"] = True
            resultado["razoes"].append("IPv6")

        # 2. Verificar VPN/Tor
        eh_vpn, msg_vpn = DetectorSegurancaAvancada.verificar_vpn_tor(ip, hostname)
        resultado["detalhes"]["vpn_tor"] = msg_vpn
        if eh_vpn:
            resultado["bloqueado"] = True
            resultado["razoes"].append("VPN/Tor")

        # 3. Verificar VM
        eh_vm, msg_vm = DetectorSegurancaAvancada.verificar_vm(user_agent, hostname)
        resultado["detalhes"]["vm"] = msg_vm
        if eh_vm:
            resultado["bloqueado"] = True
            resultado["razoes"].append("Máquina Virtual")

        # 4. Verificar GPU Cloud
        eh_gpu_cloud, msg_gpu_cloud = DetectorSegurancaAvancada.verificar_gpu_cloud(ip, hostname)
        resultado["detalhes"]["gpu_cloud"] = msg_gpu_cloud
        if eh_gpu_cloud:
            resultado["bloqueado"] = True
            resultado["razoes"].append("GPU Cloud")

        # Resumo
        if resultado["bloqueado"]:
            resultado["status"] = "🚫 BLOQUEADO"
            resultado["mensagem"] = f"Acesso negado. Razões: {', '.join(resultado['razoes'])}"
            logger.warning(f"🚫 BLOQUEIO: {resultado['ip']} - {resultado['razoes']}")
        else:
            resultado["status"] = "✅ PERMITIDO"
            resultado["mensagem"] = "Acesso verificado e aprovado"
            logger.info(f"✅ PERMITIDO: {resultado['ip']}")

        return resultado


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("🔒 DETECTOR DE SEGURANÇA AVANÇADA - TESTES")
    print("=" * 80)

    # Testes simulados
    testes = [
        {
            "nome": "IPv6 Real",
            "ip": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            "user_agent": "Mozilla/5.0",
            "hostname": "cliente-real.com"
        },
        {
            "nome": "VPN NordVPN",
            "ip": "37.19.192.100",
            "user_agent": "Mozilla/5.0",
            "hostname": "exit.nordvpn.com"
        },
        {
            "nome": "Tor Exit Node",
            "ip": "185.112.45.50",
            "user_agent": "Mozilla/5.0",
            "hostname": "tor-exit.example.com"
        },
        {
            "nome": "AWS Lambda",
            "ip": "52.45.123.200",
            "user_agent": "Mozilla/5.0",
            "hostname": "lambda.amazonaws.com"
        },
        {
            "nome": "Google Colab",
            "ip": "34.67.123.45",
            "user_agent": "Colab-GPU",
            "hostname": "colab.research.google.com"
        },
        {
            "nome": "VirtualBox",
            "ip": "192.168.1.100",
            "user_agent": "Mozilla/5.0 VirtualBox",
            "hostname": "virtualbox-vm"
        },
        {
            "nome": "IP Limpo",
            "ip": "203.45.123.200",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "hostname": "cliente.com"
        }
    ]

    for teste in testes:
        print(f"\n📋 Teste: {teste['nome']}")
        print(f"   IP: {teste['ip']}")
        print(f"   Hostname: {teste['hostname']}")
        
        resultado = DetectorSegurancaAvancada.verificacao_completa(
            teste["ip"],
            teste["user_agent"],
            teste["hostname"]
        )

        print(f"   Status: {resultado['status']}")
        print(f"   Mensagem: {resultado['mensagem']}")
        if resultado["razoes"]:
            print(f"   Razões bloqueio: {', '.join(resultado['razoes'])}")
        print(f"   Detalhes:")
        for chave, valor in resultado["detalhes"].items():
            print(f"      • {chave}: {valor}")

    print("\n" + "=" * 80)
    print("✅ TESTES CONCLUÍDOS")
    print("=" * 80)
