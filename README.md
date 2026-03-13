# Zabbix Host Import via CSV (SNMP)

![Python](https://img.shields.io/badge/Python-3.x-blue)
![API](https://img.shields.io/badge/API-Zabbix-green)
![Automation](https://img.shields.io/badge/Automation-Network%20Monitoring-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

Script em **Python** para automação de cadastro de hosts no **Zabbix** utilizando a **API oficial** e um arquivo **CSV** como fonte de dados.

Este projeto permite importar dispositivos de rede de forma rápida e padronizada, configurando automaticamente:

* Interface **SNMP**
* **Hostgroup**
* **Template**
* **Macro SNMP**
* **SNMP Community**

Ideal para ambientes de **NOC**, automação de infraestrutura ou onboarding de novos equipamentos.

---

# 📌 Objetivo

Automatizar o processo de criação de hosts no Zabbix, evitando cadastro manual no frontend.

O script foi desenvolvido para facilitar a importação em massa de dispositivos como:

* Switches
* Roteadores
* OLTs
* Firewalls
* Equipamentos de rede monitorados via SNMP

---

# ⚙️ Funcionamento do Script

O fluxo de execução segue as etapas abaixo:

```
CSV -> Script Python -> API Zabbix -> Criação do Host
```

Fluxo detalhado:

1. O script lê o arquivo **hosts.csv**
2. Para cada linha ele consulta a API do Zabbix para obter:

   * ID do Hostgroup
   * ID do Template
3. Após obter essas informações, o script executa:

```
host.create
```

4. O host é criado com interface SNMP e macros configuradas.

---

# 🗂 Estrutura do Projeto

```
.
├── import_hosts.py
├── hosts.csv
└── README.md
```

---

# 📄 Estrutura do CSV

O arquivo `hosts.csv` deve seguir o formato abaixo:

```csv
hostname,ip,group,template,community
sw-core-01,10.0.0.10,Switches,ICMP-SW-Base,public
sw-core-02,10.0.0.11,Switches,ICMP-SW-Base,public
sw-core-03,10.0.0.12,Switches,ICMP-SW-Base,monitor
```

### Campos

| Campo     | Descrição                         |
| --------- | --------------------------------- |
| hostname  | Nome do host no Zabbix            |
| ip        | Endereço IP do equipamento        |
| group     | Hostgroup onde o host será criado |
| template  | Template que será aplicado        |
| community | Community SNMP do dispositivo     |

---

# 🖧 Configuração do Host Criado

O host será criado com interface SNMP configurada da seguinte forma:

```
Type: SNMP
IP: <ip do CSV>
Port: 161
Version: SNMPv2
Community: {$SNMP_COMMUNITY}
```

Macro criada automaticamente no host:

```
{$SNMP_COMMUNITY} = <community definida no CSV>
```

Isso permite alterar a community posteriormente apenas modificando a macro.

---

# 🔑 Autenticação via API Token

O script utiliza **API Token** para autenticação na API do Zabbix.

Configuração no script:

```python
ZABBIX_URL = "http://SEU_ZABBIX/api_jsonrpc.php"
ZABBIX_TOKEN = "SEU_TOKEN"
```

O token é enviado no header HTTP:

```
Authorization: Bearer TOKEN
```

---

# 📦 Dependências

Instale a biblioteca necessária:

```bash
pip install requests
```

---

# ▶️ Como Executar

1. Configure a URL do Zabbix e o API Token no script
2. Crie o arquivo `hosts.csv`
3. Execute o script

```bash
python3 import_hosts.py
```

Exemplo de saída:

```
Importando: sw-core-01
Host criado: sw-core-01

Importando: sw-core-02
Host criado: sw-core-02
```

---

# 📡 Chamadas da API Utilizadas

O script utiliza os seguintes métodos da API do Zabbix:

### Buscar Hostgroup

```
hostgroup.get
```

### Buscar Template

```
template.get
```

### Criar Host

```
host.create
```

---

# 🔍 Exemplo de Payload da API

Criação de host:

```json
{
 "host": "sw-core-01",
 "interfaces": [
   {
     "type": 2,
     "ip": "10.0.0.10",
     "port": "161"
   }
 ],
 "groups": [
   {
     "groupid": "15"
   }
 ],
 "templates": [
   {
     "templateid": "10215"
   }
 ]
}
```

---

# ⚠️ Troubleshooting

### Template não encontrado

Verifique se o nome do template no CSV é **exatamente igual** ao existente no Zabbix.

---

### Grupo não encontrado

Verifique se o **Hostgroup existe no Zabbix** e se o nome está correto.

---

### Erro de autenticação

Confirme se:

* O API Token está válido
* O usuário possui permissão para criar hosts

---

# 💡 Possíveis Melhorias

Algumas melhorias que podem ser implementadas no script:

* Verificação de **host duplicado**
* Criação automática de **hostgroups**
* Suporte a **SNMP v3**
* Suporte a **proxy**
* Aplicação de **múltiplos templates**
* Importação de **tags**
* Importação de **macros adicionais**
* Cache de templates e grupos (melhor performance)

---

# 🚀 Casos de Uso

Este script pode ser utilizado para:

* Onboarding automatizado de equipamentos
* Provisionamento de monitoramento
* Automação de NOC
* Integração com inventários de rede
* Importação em massa de dispositivos

---

# 📜 Licença

MIT License.

Uso livre para fins educacionais e automação de ambientes de monitoramento.

---

# 👨‍💻 Autor

Projeto desenvolvido para automação de monitoramento no **Zabbix**, utilizando Python e API oficial.

Se este projeto te ajudou, considere ⭐ o repositório.
