from ophyd import Component as Cpt

from bluesky_handling.visa_signal import VISA_Signal_Write, VISA_Signal_Read, VISA_Device



class Keithley_2000(VISA_Device):
    V_DC = Cpt(VISA_Signal_Read, name='V_DC')
    V_AC = Cpt(VISA_Signal_Read, name='V_AC')
    I_DC = Cpt(VISA_Signal_Read, name='I_DC')
    I_AC = Cpt(VISA_Signal_Read, name='I_AC')
    resistance = Cpt(VISA_Signal_Read, name='resistance')
    resistance_4_wire = Cpt(VISA_Signal_Read, name='resistance_4_wire')

    NPLC = Cpt(VISA_Signal_Write, name='NPLC', kind='config')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='',
                 **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         resource_name=resource_name, baud_rate=19200, write_termination='\r', read_termination='\r', **kwargs)
        self.last_meas = ''
        self.nplc = 1
        self.V_DC.read_function = lambda: self.query_function('VOLT:DC')
        self.V_AC.read_function = lambda: self.query_function('VOLT:AC')
        self.I_DC.read_function = lambda: self.query_function('CURR:DC')
        self.I_AC.read_function = lambda: self.query_function('CURR:AC')
        self.resistance.read_function = lambda: self.query_function('RES')
        self.resistance_4_wire.read_function = lambda: self.query_function('FRES')
        self.NPLC.put_conv_function = self.NPLC_func
        # self.visa_instrument.write('*RST')
        # a = self.visa_instrument.query('*idn?')
        # print(a)
        for comp in self.walk_signals():
            it = comp.item
            it.match_return = True

    def NPLC_func(self, val):
        self.nplc = val
        # w_str = f':VOLT:DC:NPLC {val}\r\n'
        # w_str += f':VOLT:AC:NPLC {val}\r\n'
        # w_str += f':CURR:DC:NPLC {val}\r\n'
        # w_str += f':CURR:AC:NPLC {val}\r\n'
        # w_str += f':RES:NPLC {val}\r\n'
        # w_str += f':FRES:NPLC {val}'
        return ''

    def query_function(self, meas):
        if meas != self.last_meas:
            self.visa_instrument.write(f'CONF:{meas}')
            self.visa_instrument.write(f':{meas}:NPLC {self.nplc}')
            self.last_meas = meas
        else:
            self.visa_instrument.write('INIT')
        return 'DATA?'
