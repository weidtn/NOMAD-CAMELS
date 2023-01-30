from ophyd import Component as Cpt
from bluesky_handling.visa_signal import VISA_Device, VISA_Signal_Read, VISA_Signal_Write
from bluesky_handling.custom_function_signal import Custom_Function_SignalRO, Custom_Function_Signal

ADC_range_values = ["100 nA", "1 uA", "10 uA", "100 uA", "1 mA", "10 mA"]

class Gap_Burner_Arduino(VISA_Device):
    ramp_time = Cpt(Custom_Function_Signal, name="ramp_time", kind='config', additional_put_text='ramp_time ')
    offset = Cpt(Custom_Function_Signal, name="offset", kind='config', additional_put_text='offset ')
    min_current = Cpt(Custom_Function_Signal, name="min_current", kind='config', additional_put_text='min_current ')
    min_voltage = Cpt(Custom_Function_Signal, name="min_voltage", kind='config', additional_put_text='min_voltage ')
    dac_ref_zero = Cpt(Custom_Function_Signal, name="dac_ref_zero", kind='config', additional_put_text='dac_ref_zero ')
    dac_zero = Cpt(Custom_Function_Signal, name="dac_zero", kind='config', additional_put_text='dac_zero ')
    idn = Cpt(VISA_Signal_Read, name='idn', kind='config', query_text='*IDN?')

    output_range = Cpt(Custom_Function_Signal, name="output_range")
    input_range = Cpt(Custom_Function_Signal, name="input_range")
    lowpass_samples = Cpt(Custom_Function_Signal, name="lowpass_samples")
    threshold = Cpt(Custom_Function_Signal, name="threshold")

    burn_command = Cpt(Custom_Function_Signal, name='burn_command')
    iv_curve = Cpt(Custom_Function_SignalRO, name='iv_curve')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='',
                 baud_rate=9600, write_termination='\r\n',
                 read_termination='\r\n', **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         resource_name=resource_name, baud_rate=baud_rate,
                         write_termination=write_termination,
                         read_termination=read_termination, **kwargs)

        self.ramp_time.put_function = lambda x: self.param('ramp_time', x)
        self.offset.put_function = lambda x: self.param('offset', x)
        self.min_current.put_function = lambda x: self.param('min_current', x)
        self.min_voltage.put_function = lambda x: self.param('min_voltage', x)
        self.dac_ref_zero.put_function = lambda x: self.param('dac_ref_zero', x)
        self.dac_zero.put_function = lambda x: self.param('dac_zero', x)

        self.lowpass_samples.put_function = lambda x: self.param("lowpass_samples", x)
        self.threshold.put_function = lambda x: self.param("threshold", x)
        self.output_range.put_function = self.out_range_func
        self.input_range.put_function = self.input_range_func

        self.burn_command.put_function = self.burn
        self.iv_curve.read_function = self.iv

    def get_iv_curve(self):
        self.visa_instrument.query('iv?')


    def write(self, cmd: str):
        if self.visa_instrument is None:
            print("Tried to write while disconnected")
        else:
            self.visa_instrument.write(cmd, termination='\n')
            print("Arduino << " + cmd)

    def input_range_func(self, val):
        self.visa_instrument.write(f'input_range {ADC_range_values[int(val)]}')
        ok = self.visa_instrument.read(termination='\n')
        print("Arduino >> " + ok)

    def out_range_func(self, val):
        self.visa_instrument.write(f'output_range {val:d} V')
        ok = self.visa_instrument.read(termination='\n')
        print("Arduino >> " + ok)

    def query(self, cmd: str):
        if self.visa_instrument is None:
            print("Tried to query while disconnected")
            return None

        print("Arduino << " + cmd)
        self.visa_instrument.write(cmd, termination='\n')

        error = self.visa_instrument.read(termination='\n')

        if error == "OK":
            print("Arduino >> OK")
            value = self.visa_instrument.read(termination='\n')
            print("Arduino >> " + value)
            return value
        else:
            print(error)
            return None


    def param(self, name: str, value):
        self.write("%s %s" % (name, str(value)))
        ok = self.visa_instrument.read(termination='\n')
        print("Arduino >> " + ok)


    def burn(self, val):
        self.write('burn')
        ok = self.visa_instrument.read(termination='\n')
        print("Arduino >> " + ok)
        return ok


    def iv(self):
        self.write('iv?')
        ok = self.visa_instrument.read(termination='\n')
        data = self.visa_instrument.read_ascii_values(converter='d')
        print("Arduino >> <%d ADC values>" % len(data))
        return data

