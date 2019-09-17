from . import dns
from . import protocol


async def query(dns_server, domain, record_type):
    m = await dns.Message.create_question(domain, record_type)
    return await protocol.UdpClient.send_message(m, dns_server)