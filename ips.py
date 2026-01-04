import socket
import sys
import time
from datetime import datetime

# Cores para terminal (opcional)
class Cores:
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    CIANO = '\033[96m'
    BRANCO = '\033[97m'
    RESET = '\033[0m'
    NEGRITO = '\033[1m'

def banner():
    """Exibe o banner do programa"""
    print(Cores.CIANO + """
╔═══════════════════════════════════════╗
║          ██╗██████╗ ███████╗          ║
║          ██║██╔══██╗██╔════╝          ║
║          ██║██████╔╝███████╗          ║
║     ██   ██║██╔═══╝ ╚════██║          ║
║     ╚█████╔╝██║     ███████║          ║
║      ╚════╝ ╚═╝     ╚══════╝          ║
║            ips1.0 v1.0                ║
║    Descobridor de IP de Sites         ║
╚═══════════════════════════════════════╝
""" + Cores.RESET)

def obter_ip(site):
    """
    Função para obter o endereço IP de um site/domínio
    """
    try:
        # Limpa a URL
        site = site.lower().strip()
        if site.startswith(('http://', 'https://')):
            site = site.split('://')[1]
        site = site.rstrip('/').split('/')[0]
        
        print(f"\n{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
        print(f"{Cores.NEGRITO}🔍 Analisando:{Cores.RESET} {Cores.CIANO}{site}{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
        
        print(f"{Cores.AMARELO}⏳ Resolvendo DNS...{Cores.RESET}")
        time.sleep(0.5)
        
        # Obtém o endereço IP
        ip = socket.gethostbyname(site)
        
        print(f"{Cores.VERDE}✅ IP encontrado!{Cores.RESET}")
        time.sleep(0.3)
        
        # Informações detalhadas
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        print(f"\n{Cores.NEGRITO}📋 RESULTADO:{Cores.RESET}")
        print(f"{Cores.BRANCO}┌──────────────────────────────────────┐{Cores.RESET}")
        print(f"{Cores.BRANCO}│{Cores.RESET} {Cores.NEGRITO}Domínio:{Cores.RESET} {Cores.CIANO}{site:30}{Cores.RESET} {Cores.BRANCO}│{Cores.RESET}")
        print(f"{Cores.BRANCO}│{Cores.RESET} {Cores.NEGRITO}Endereço IP:{Cores.RESET} {Cores.VERDE}{ip:25}{Cores.RESET} {Cores.BRANCO}│{Cores.RESET}")
        print(f"{Cores.BRANCO}│{Cores.RESET} {Cores.NEGRITO}Data/Hora:{Cores.RESET} {agora:26} {Cores.BRANCO}│{Cores.RESET}")
        print(f"{Cores.BRANCO}└──────────────────────────────────────┘{Cores.RESET}")
        
        # Informações adicionais
        try:
            print(f"\n{Cores.AMARELO}📊 Informações adicionais:{Cores.RESET}")
            print(f"   • Classe do IP: {classificar_ip(ip)}")
            print(f"   • Tipo: Público" if is_ip_publico(ip) else "   • Tipo: Privado/Reservado")
            
        except:
            pass
            
        return ip
        
    except socket.gaierror:
        print(f"\n{Cores.VERMELHO}❌ ERRO: Não foi possível resolver '{site}'{Cores.RESET}")
        print(f"{Cores.AMARELO}   Verifique:{Cores.RESET}")
        print(f"   • Ortografia do domínio")
        print(f"   • Conexão com a internet")
        print(f"   • Se o site existe")
        return None
        
    except Exception as e:
        print(f"\n{Cores.VERMELHO}⚠️ Erro inesperado: {e}{Cores.RESET}")
        return None

def classificar_ip(ip):
    """Classifica o IP por classe"""
    primeiro_octeto = int(ip.split('.')[0])
    
    if 1 <= primeiro_octeto <= 126:
        return "Classe A"
    elif 128 <= primeiro_octeto <= 191:
        return "Classe B"
    elif 192 <= primeiro_octeto <= 223:
        return "Classe C"
    elif 224 <= primeiro_octeto <= 239:
        return "Classe D (Multicast)"
    elif 240 <= primeiro_octeto <= 255:
        return "Classe E (Experimental)"
    else:
        return "Desconhecida"

def is_ip_publico(ip):
    """Verifica se o IP é público"""
    octetos = list(map(int, ip.split('.')))
    
    # IPs privados
    if octetos[0] == 10:
        return False
    if octetos[0] == 172 and 16 <= octetos[1] <= 31:
        return False
    if octetos[0] == 192 and octetos[1] == 168:
        return False
    if octetos[0] == 169 and octetos[1] == 254:
        return False  # Link-local
    
    # Loopback
    if octetos[0] == 127:
        return False
        
    # Multcast
    if 224 <= octetos[0] <= 239:
        return False
        
    return True

def scan_multiplos():
    """Escaneia múltiplos sites de uma vez"""
    print(f"\n{Cores.MAGENTA}📝 Modo Scan Multiplo{Cores.RESET}")
    print(f"{Cores.AMARELO}Digite os sites (um por linha). Digite 'fim' para terminar:{Cores.RESET}\n")
    
    sites = []
    contador = 1
    
    while True:
        site = input(f"  {contador:2d}> ").strip()
        if site.lower() in ['fim', 'exit', 'sair', '']:
            break
        if site:
            sites.append(site)
            contador += 1
    
    if not sites:
        print(f"{Cores.VERMELHO}Nenhum site informado.{Cores.RESET}")
        return
    
    print(f"\n{Cores.VERDE}🎯 Iniciando scan de {len(sites)} site(s)...{Cores.RESET}")
    
    resultados = []
    for i, site in enumerate(sites, 1):
        print(f"\n{Cores.BRANCO}[{i:02d}/{len(sites):02d}]{Cores.RESET}", end=" ")
        ip = obter_ip(site)
        if ip:
            resultados.append((site, ip))
        time.sleep(0.2)
    
    if resultados:
        print(f"\n{Cores.VERDE}📊 RESUMO DO SCAN:{Cores.RESET}")
        print(f"{Cores.BRANCO}┌{'─'*35}┐{Cores.RESET}")
        for site, ip in resultados:
            print(f"{Cores.BRANCO}│{Cores.RESET} {site:25} {Cores.VERDE}→{Cores.RESET} {ip:15} {Cores.BRANCO}│{Cores.RESET}")
        print(f"{Cores.BRANCO}└{'─'*35}┘{Cores.RESET}")

def sites_populares():
    """Testa sites populares automaticamente"""
    sites = [
        "google.com",
        "facebook.com",
        "youtube.com",
        "instagram.com",
        "twitter.com",
        "github.com",
        "whatsapp.com",
        "netflix.com",
        "amazon.com",
        "microsoft.com"
    ]
    
    print(f"\n{Cores.MAGENTA}🌐 Testando Sites Populares{Cores.RESET}")
    print(f"{Cores.AMARELO}Escaneando 10 sites mais acessados...{Cores.RESET}")
    
    resultados = []
    for i, site in enumerate(sites, 1):
        print(f"\n{Cores.BRANCO}[{i:02d}/10]{Cores.RESET}", end=" ")
        ip = obter_ip(site)
        if ip:
            resultados.append((site, ip))
        time.sleep(0.3)
    
    return resultados

def exportar_resultados(resultados, arquivo="ips_resultados.txt"):
    """Exporta resultados para um arquivo"""
    try:
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write("="*50 + "\n")
            f.write("RESULTADOS IPS1.0\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            
            for site, ip in resultados:
                f.write(f"🔗 {site}\n")
                f.write(f"   IP: {ip}\n")
                f.write(f"   Classe: {classificar_ip(ip)}\n")
                f.write(f"   Tipo: {'Público' if is_ip_publico(ip) else 'Privado/Reservado'}\n")
                f.write("-"*30 + "\n")
        
        print(f"{Cores.VERDE}💾 Resultados exportados para: {arquivo}{Cores.RESET}")
        return True
    except Exception as e:
        print(f"{Cores.VERMELHO}❌ Erro ao exportar: {e}{Cores.RESET}")
        return False

def menu_principal():
    """Menu principal do programa"""
    while True:
        print(f"\n{Cores.AZUL}════════════════ MENU PRINCIPAL ════════════════{Cores.RESET}")
        print(f"{Cores.CIANO}1.{Cores.RESET} {Cores.NEGRITO}Buscar IP de um site{Cores.RESET}")
        print(f"{Cores.CIANO}2.{Cores.RESET} {Cores.NEGRITO}Buscar múltiplos sites{Cores.RESET}")
        print(f"{Cores.CIANO}3.{Cores.RESET} {Cores.NEGRITO}Sites populares (automático){Cores.RESET}")
        print(f"{Cores.CIANO}4.{Cores.RESET} {Cores.NEGRITO}Sobre o programa{Cores.RESET}")
        print(f"{Cores.CIANO}5.{Cores.RESET} {Cores.NEGRITO}Sair{Cores.RESET}")
        print(f"{Cores.AZUL}═════════════════════════════════════════════════{Cores.RESET}")
        
        try:
            opcao = input(f"\n{Cores.VERDE}ips1.0>{Cores.RESET} ").strip()
            
            if opcao == '1':
                site = input(f"\n{Cores.CIANO}Digite o site (ex: google.com): {Cores.RESET}").strip()
                if site:
                    obter_ip(site)
                else:
                    print(f"{Cores.VERMELHO}❌ Nenhum site informado.{Cores.RESET}")
                    
            elif opcao == '2':
                scan_multiplos()
                
            elif opcao == '3':
                resultados = sites_populares()
                if resultados:
                    exportar = input(f"\n{Cores.AMARELO}Exportar resultados? (S/N): {Cores.RESET}").lower()
                    if exportar in ['s', 'sim']:
                        exportar_resultados(resultados)
                        
            elif opcao == '4':
                print(f"""
{Cores.CIANO}┌────────────────────────────────────────────┐{Cores.RESET}
{Cores.CIANO}│          SOBRE O IPS1.0 v1.0              │{Cores.RESET}
{Cores.CIANO}├────────────────────────────────────────────┤{Cores.RESET}
{Cores.CIANO}│                                            │{Cores.RESET}
{Cores.CIANO}│  {Cores.VERDE}✓{Cores.CIANO} Descobre IPs de sites na internet  │{Cores.RESET}
{Cores.CIANO}│  {Cores.VERDE}✓{Cores.CIANO} Funciona no Termux                 │{Cores.RESET}
{Cores.CIANO}│  {Cores.VERDE}✓{Cores.CIANO} Interface colorida                 │{Cores.RESET}
{Cores.CIANO}│  {Cores.VERDE}✓{Cores.CIANO} Exporta resultados para arquivo    │{Cores.RESET}
{Cores.CIANO}│                                            │{Cores.RESET}
{Cores.CIANO}│  {Cores.AMARELO}Uso:{Cores.CIANO} python ips1.0.py [site]       │{Cores.RESET}
{Cores.CIANO}│  {Cores.AMARELO}Ex:{Cores.CIANO} python ips1.0.py google.com    │{Cores.RESET}
{Cores.CIANO}│                                            │{Cores.RESET}
{Cores.CIANO}└────────────────────────────────────────────┘{Cores.RESET}
                """)
                
            elif opcao == '5':
                print(f"\n{Cores.VERDE}👋 Obrigado por usar ips1.0! Até logo!{Cores.RESET}")
                break
                
            else:
                print(f"{Cores.VERMELHO}❌ Opção inválida! Use 1-5.{Cores.RESET}")
                
        except KeyboardInterrupt:
            print(f"\n\n{Cores.AMARELO}⚠️ Interrompido pelo usuário.{Cores.RESET}")
            continuar = input(f"\n{Cores.AMARELO}Deseja realmente sair? (S/N): {Cores.RESET}").lower()
            if continuar in ['s', 'sim']:
                print(f"{Cores.VERDE}👋 Até logo!{Cores.RESET}")
                break

def modo_rapido(sites):
    """Modo rápido via linha de comando"""
    print(f"{Cores.VERDE}🚀 Modo rápido - Processando {len(sites)} site(s){Cores.RESET}")
    
    resultados = []
    for site in sites:
        ip = obter_ip(site)
        if ip:
            resultados.append((site, ip))
    
    if len(resultados) > 1:
        exportar_resultados(resultados)

def main():
    """Função principal"""
    banner()
    
    # Verifica se tem argumentos
    if len(sys.argv) > 1:
        # Modo linha de comando rápido
        modo_rapido(sys.argv[1:])
    else:
        # Modo interativo
        print(f"{Cores.AMARELO}📱 Executando no Termux | Python {sys.version.split()[0]}{Cores.RESET}")
        print(f"{Cores.CIANO}Digite 'help' para ajuda ou selecione uma opção abaixo{Cores.RESET}")
        
        # Pequena pausa para efeito visual
        time.sleep(0.5)
        menu_principal()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Cores.VERMELHO}❌ Programa interrompido.{Cores.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Cores.VERMELHO}💥 Erro crítico: {e}{Cores.RESET}")
        sys.exit(1)
