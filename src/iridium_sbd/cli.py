import click
import serial
import time

from adafruit_rockblock import RockBlock


device_info = dict()


def update_device_info(rb: RockBlock):
    device_info['Status'] = rb.status
    device_info['Model'] = rb.model
    for item in rb.revision:
        elements = item.split(':')
        device_info[elements[0]] = elements[1][1:]

    device_info['Serial Number'] = rb.serial_number
    device_info['Geolocation'] = f"{rb.geolocation[:-1]} {time.strftime('%Y-%m-%dT%H:%M:%SZ', rb.geolocation[-1])}"
    device_info['System time'] = time.strftime(
        '%Y-%m-%dT%H:%M:%SZ', rb.system_time)


def print_device_info():
    for item in device_info.items():
        k, v = item
        print("{:<23} | {:<15}".format(k, str(v)))


def sbd_transfer(rb:RockBlock):
    # try a satellite Short Burst Data transfer
    print("Talking to satellite...")
    status = rb.satellite_transfer()
    # loop as needed
    retry = 0
    while status[0] > 8:
        time.sleep(10)
        status = rb.satellite_transfer()
        print(retry, status)
        retry += 1


@click.group()
@click.option('--serial_device', default="/dev/ttyUSB0", help='Serial device path.')
@click.pass_context
def cli(ctx, serial_device: str):
    ctx.serial_device = serial_device

    with serial.Serial(serial_device, baudrate=19200, bytesize=serial.EIGHTBITS,
                       parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                       xonxoff=False, timeout=1) as serial_conn:

        rb = RockBlock(serial_conn)
        update_device_info(rb)
        print_device_info()


@cli.command()
@click.option('--message', default="Hello world from space!", help='Message to send.')
@click.pass_context
def send(ctx, message):
    with serial.Serial(ctx.parent.serial_device, baudrate=19200, bytesize=serial.EIGHTBITS,
                       parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                       xonxoff=False, timeout=1) as serial_conn:

        rb = RockBlock(serial_conn)
        # set the text
        rb.text_out = message

        sbd_transfer(rb)
        print("\nDONE.")


@cli.command()
@click.pass_context
def receive(ctx):
    with serial.Serial(ctx.parent.serial_device, baudrate=19200, bytesize=serial.EIGHTBITS,
                       parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                       xonxoff=False, timeout=1) as serial_conn:

        rb = RockBlock(serial_conn)

        sbd_transfer(rb)
        print("\nDONE.")

        # get the text
        print(rb.text_in)


@cli.command()
@click.pass_context
def signal(ctx):
    with serial.Serial(ctx.parent.serial_device, baudrate=19200, bytesize=serial.EIGHTBITS,
                       parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                       xonxoff=False, timeout=1) as serial_conn:

        rb = RockBlock(serial_conn)

        while True:

            resp = rb._uart_xfer("+CSQ")

            if resp[-1].strip().decode() == "OK":
                signal_level = int(resp[-3].strip().decode().split(":")[1])
            else:
                signal_level = 0

            click.clear()
            print_device_info()
            print('\nPress CTR+C to exit\n')
            with click.progressbar(label='Signal', empty_char=' ', length=5, show_pos=True) as bar:
                bar.update(signal_level)

            time.sleep(0.5)


if __name__ == '__main__':
    cli()
