class Iridium9603:
    """Library for the Iridium SDB 9603
    :param uart: The UART devce the Iridium SDB 9603 is connected to.
    """

    def __init__(self, serial):
        self._serial = serial
        self.status = self.status()
        self.model = self._atcmd('AT+CGMM', 2)
        self.manufacturer = self._atcmd('AT+CGMI', 2)
        self.imei = int(self._atcmd('AT+GSN', 2))

    def _atcmd(self, command: str, response_lenght: int) -> str:
        cmd = command + '\r'
        self._serial.write(cmd.encode())

        response = [r.decode().rstrip() for r in self._serial.readlines()
                    if cmd not in r.decode() and r.decode().rstrip() != '']

        if 'OK' in response and len(response) == response_lenght:
            return response[0]
        else:
            return 'UNKNOWN'

    def status(self):
        return self._atcmd('AT', 1)

    def signal_strength(self):
        return self._atcmd('AT+CSQ', 2)
