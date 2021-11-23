import click
import serial

from iridium_sbd.iridium_9603 import Iridium9603


@click.group()
@click.option('--serial_device', default="/dev/ttyUSB0", help='Serial device path.')
@click.pass_context
def cli(ctx, serial_device: str):
    ctx.serial_device = serial_device

    with serial.Serial(serial_device, baudrate=19200, bytesize=serial.EIGHTBITS,
                       parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                       xonxoff=False, timeout=1) as serial_conn:

        iridium = Iridium9603(serial=serial_conn)

        for item in iridium.__dict__.items():
            k, v = item
            if '_' not in k:
                print("{:<12} | {:<15}".format(k, str(v)))


@cli.command()
@click.pass_context
def signal_strength(ctx):
    with serial.Serial(ctx.parent.serial_device, baudrate=19200, bytesize=serial.EIGHTBITS,
                       parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                       xonxoff=False, timeout=1) as serial_conn:

        iridium = Iridium9603(serial=serial_conn)
        print(f"\nSignal Strength: {iridium.signal_strength()}")
