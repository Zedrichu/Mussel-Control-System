#Python
# -*- coding: utf-8 -*-
"""
Thermistor.

Description: Class defining thermal sensing device with linearized ADC voltages.

@__Author --> Created by Luca Pezzarossa & Adrian Zvizdenco & Jeppe Mikkelsen
@__Date & Time --> Created on 06/06/2022
@__Version --> = 1.1
@__Status --> = Test
"""

from machine import Pin, ADC, DAC
from math import log

import machine
import utime

# Perform linearization with the file LinearizationADC.py (copy results in arrauy)
adc_V_lookup = [0.02470588, 0.01544118, 0.03088236, 0.04632353, 0.06176471, 0.06588235, 0.07, 0.07411765, 0.07720589, 0.08029412, 0.08338236, 0.08647059, 0.09058825, 0.09470588, 0.09882354, 0.1029412, 0.1070588, 0.1111765, 0.1152941, 0.1194118, 0.1235294, 0.1266177, 0.1297059, 0.1327941, 0.1358824, 0.1389706, 0.1420588, 0.1451471, 0.1482353, 0.1513235, 0.1544118, 0.1575, 0.1605882, 0.1647059, 0.1688235, 0.1729412, 0.1760294, 0.1791177, 0.1822059, 0.1852941, 0.1877647, 0.1902353, 0.1927059, 0.1951765, 0.1976471, 0.2017647, 0.2058824, 0.21, 0.2130883, 0.2161765, 0.2192647, 0.222353, 0.2264706, 0.2305882, 0.2347059, 0.2377941, 0.2408824, 0.2439706, 0.2470588, 0.2511765, 0.2552941, 0.2594118, 0.2625, 0.2655883, 0.2686765, 0.2717647, 0.2758824, 0.28, 0.2841177, 0.2882353, 0.2923529, 0.2964706, 0.2989412, 0.3014118, 0.3038824, 0.3063529, 0.3088235, 0.3129412, 0.3170588, 0.3211765, 0.3242647, 0.327353, 0.3304412, 0.3335294, 0.3397059, 0.3458824, 0.3489706, 0.3520588, 0.3551471, 0.3582353, 0.3613235, 0.3644118, 0.3675, 0.3705883, 0.3747059, 0.3788235, 0.3829412, 0.3860294, 0.3891177, 0.3922059, 0.3952941, 0.3994118, 0.4035295, 0.4076471, 0.4107353, 0.4138236, 0.4169118, 0.42, 0.4241177, 0.4282353, 0.432353, 0.4364706, 0.4405883, 0.4447059, 0.4477942, 0.4508824, 0.4539706, 0.4570589, 0.4611764, 0.4652942, 0.4694118, 0.4725, 0.4755883, 0.4786765, 0.4817647, 0.484853, 0.4879412, 0.4910295, 0.4941177, 0.4972059, 0.5002942, 0.5033824, 0.5064706, 0.5095589, 0.5126471, 0.5157353, 0.5188236, 0.5219118, 0.525, 0.5280883, 0.5311765, 0.5352941, 0.5394118, 0.5435295, 0.547647, 0.5517647, 0.5558824, 0.5589706, 0.5620589, 0.5651471, 0.5682353, 0.5713236, 0.5744118, 0.5775001, 0.5805883, 0.5836765, 0.5867648, 0.589853, 0.5929412, 0.5970588, 0.6011765, 0.6052941, 0.6083823, 0.6114706, 0.6145588, 0.6176471, 0.6207353, 0.6238235, 0.6269117, 0.63, 0.6341177, 0.6382353, 0.642353, 0.6454412, 0.6485294, 0.6516176, 0.6547059, 0.6577941, 0.6608824, 0.6639706, 0.6670588, 0.6711765, 0.6752942, 0.6794118, 0.6835294, 0.6876471, 0.6917647, 0.6948529, 0.6979412, 0.7010294, 0.7041177, 0.7082353, 0.712353, 0.7164706, 0.7195588, 0.7226471, 0.7257353, 0.7288236, 0.7319118, 0.735, 0.7380882, 0.7411765, 0.7452941, 0.7494118, 0.7535295, 0.7566176, 0.7597059, 0.7627941, 0.7658824, 0.77, 0.7741177, 0.7782353, 0.7802942, 0.7823529, 0.7844118, 0.7864707, 0.7885294, 0.7905883, 0.7947059, 0.7988235, 0.8029412, 0.8060294, 0.8091177, 0.8122059, 0.8152942, 0.8183824, 0.8214706, 0.8245588, 0.8276471, 0.8317648, 0.8358824, 0.8400001, 0.8430882, 0.8461765, 0.8492647, 0.852353, 0.8554412, 0.8585295, 0.8616177, 0.8647059, 0.8688236, 0.8729412, 0.8770589, 0.8811766, 0.8852942, 0.8894118, 0.8925, 0.8955883, 0.8986765, 0.9017648, 0.9058825, 0.91, 0.9141177, 0.9165882, 0.9190589, 0.9215294, 0.9240001, 0.9264707, 0.9295588, 0.9326471, 0.9357353, 0.9388236, 0.9419118, 0.9450001, 0.9480883, 0.9511765, 0.9552942, 0.9594117, 0.9635295, 0.9666177, 0.969706, 0.9727942, 0.9758824, 0.9789706, 0.9820589, 0.9851471, 0.9882354, 0.9913236, 0.9944118, 0.9975, 1.000588, 1.003677, 1.006765, 1.009853, 1.012941, 1.017059, 1.021176, 1.025294, 1.028382, 1.031471, 1.034559, 1.037647, 1.041765, 1.045882, 1.05, 1.052471, 1.054941, 1.057412, 1.059882, 1.062353, 1.066471, 1.070588, 1.074706, 1.078824, 1.082941, 1.087059, 1.090147, 1.093235, 1.096324, 1.099412, 1.1025, 1.105588, 1.108677, 1.111765, 1.115882, 1.12, 1.124118, 1.127206, 1.130294, 1.133382, 1.136471, 1.139559, 1.142647, 1.145735, 1.148824, 1.152941, 1.157059, 1.161177, 1.164265, 1.167353, 1.170441, 1.17353, 1.179706, 1.185882, 1.188971, 1.192059, 1.195147, 1.198235, 1.201324, 1.204412, 1.2075, 1.210588, 1.213676, 1.216765, 1.219853, 1.222941, 1.227059, 1.231176, 1.235294, 1.238382, 1.241471, 1.244559, 1.247647, 1.250735, 1.253824, 1.256912, 1.26, 1.264118, 1.268235, 1.272353, 1.275441, 1.278529, 1.281618, 1.284706, 1.288824, 1.292941, 1.297059, 1.301177, 1.305294, 1.309412, 1.3125, 1.315588, 1.318676, 1.321765, 1.325882, 1.33, 1.334118, 1.337206, 1.340294, 1.343382, 1.346471, 1.349559, 1.352647, 1.355735, 1.358824, 1.361294, 1.363765, 1.366235, 1.368706, 1.371176, 1.373647, 1.376118, 1.378588, 1.381059, 1.383529, 1.387647, 1.391765, 1.395882, 1.4, 1.404118, 1.408235, 1.411324, 1.414412, 1.4175, 1.420588, 1.423676, 1.426765, 1.429853, 1.432941, 1.436029, 1.439118, 1.442206, 1.445294, 1.449412, 1.453529, 1.457647, 1.460735, 1.463824, 1.466912, 1.47, 1.474118, 1.478235, 1.482353, 1.485441, 1.488529, 1.491618, 1.494706, 1.498824, 1.502941, 1.507059, 1.511177, 1.515294, 1.519412, 1.5225, 1.525588, 1.528677, 1.531765, 1.534853, 1.537941, 1.541029, 1.544118, 1.547206, 1.550294, 1.553382, 1.556471, 1.560588, 1.564706, 1.568824, 1.571912, 1.575, 1.578088, 1.581177, 1.584265, 1.587353, 1.590441, 1.593529, 1.596618, 1.599706, 1.602794, 1.605882, 1.61, 1.614118, 1.618235, 1.622353, 1.626471, 1.630588, 1.633677, 1.636765, 1.639853, 1.642941, 1.646029, 1.649118, 1.652206, 1.655294, 1.659412, 1.663529, 1.667647, 1.670735, 1.673824, 1.676912, 1.68, 1.684118, 1.688235, 1.692353, 1.695441, 1.698529, 1.701618, 1.704706, 1.707794, 1.710882, 1.713971, 1.717059, 1.723235, 1.729412, 1.7325, 1.735588, 1.738677, 1.741765, 1.745882, 1.75, 1.754118, 1.757206, 1.760294, 1.763382, 1.766471, 1.768941, 1.771412, 1.773882, 1.776353, 1.778824, 1.781294, 1.783765, 1.786235, 1.788706, 1.791177, 1.795294, 1.799412, 1.80353, 1.806618, 1.809706, 1.812794, 1.815882, 1.82, 1.824118, 1.828235, 1.831324, 1.834412, 1.8375, 1.840588, 1.843677, 1.846765, 1.849853, 1.852941, 1.857059, 1.861177, 1.865294, 1.869412, 1.87353, 1.877647, 1.880735, 1.883824, 1.886912, 1.89, 1.894118, 1.898235, 1.902353, 1.905441, 1.908529, 1.911618, 1.914706, 1.917794, 1.920882, 1.923971, 1.927059, 1.931176, 1.935294, 1.939412, 1.9425, 1.945588, 1.948677, 1.951765, 1.954853, 1.957941, 1.96103, 1.964118, 1.970294, 1.976471, 1.979559, 1.982647, 1.985735, 1.988824, 1.991912, 1.995, 1.998088, 2.001177, 2.005294, 2.009412, 2.01353, 2.017647, 2.021765, 2.025882, 2.028971, 2.032059, 2.035147, 2.038235, 2.041324, 2.044412, 2.0475, 2.050588, 2.053677, 2.056765, 2.059853, 2.062941, 2.067059, 2.071177, 2.075294, 2.079412, 2.083529, 2.087647, 2.090735, 2.093824, 2.096912, 2.1, 2.104118, 2.108235, 2.112353, 2.115441, 2.11853, 2.121618, 2.124706, 2.127794, 2.130883, 2.133971, 2.137059, 2.141176, 2.145294, 2.149412, 2.1525, 2.155588, 2.158677, 2.161765, 2.164853, 2.167941, 2.17103, 2.174118, 2.177206, 2.180294, 2.183383, 2.186471, 2.189559, 2.192647, 2.195735, 2.198824, 2.201912, 2.205, 2.208088, 2.211177, 2.215294, 2.219412, 2.22353, 2.226, 2.228471, 2.230941, 2.233412, 2.235883, 2.238971, 2.242059, 2.245147, 2.248235, 2.251324, 2.254412, 2.2575, 2.260588, 2.264706, 2.268824, 2.272941, 2.277059, 2.281177, 2.285294, 2.288383, 2.291471, 2.294559, 2.297647, 2.300735, 2.303824, 2.306912, 2.31, 2.314118, 2.318235, 2.322353, 2.325441, 2.32853, 2.331618, 2.334706, 2.338824, 2.342941, 2.347059, 2.34953, 2.352, 2.354471, 2.356941, 2.359412, 2.361882, 2.364353, 2.366824, 2.369294, 2.371765, 2.374853, 2.377941, 2.381029, 2.384118, 2.388235, 2.392353, 2.396471, 2.398941, 2.401412, 2.403883, 2.406353, 2.408823, 2.415, 2.421176, 2.423647, 2.426118, 2.428588, 2.431059, 2.433529, 2.436618, 2.439706, 2.442794, 2.445882, 2.448971, 2.452059, 2.455147, 2.458235, 2.462353, 2.466471, 2.470588, 2.473676, 2.476765, 2.479853, 2.482941, 2.486029, 2.489118, 2.492206, 2.495294, 2.498382, 2.501471, 2.504559, 2.507647, 2.510735, 2.513824, 2.516912, 2.52, 2.523088, 2.526176, 2.529265, 2.532353, 2.535441, 2.538529, 2.541618, 2.544706, 2.547177, 2.549647, 2.552118, 2.554588, 2.557059, 2.55953, 2.562, 2.564471, 2.566941, 2.569412, 2.5725, 2.575588, 2.578676, 2.581765, 2.584235, 2.586706, 2.589177, 2.591647, 2.594118, 2.597206, 2.600294, 2.603382, 2.606471, 2.608941, 2.611412, 2.613883, 2.616353, 2.618824, 2.621294, 2.623765, 2.626235, 2.628706, 2.631176, 2.634265, 2.637353, 2.640441, 2.643529, 2.645588, 2.647647, 2.649706, 2.651765, 2.653824, 2.655882, 2.66, 2.664118, 2.668235, 2.671324, 2.674412, 2.6775, 2.680588, 2.683059, 2.685529, 2.688, 2.690471, 2.692941, 2.695412, 2.697882, 2.700353, 2.702824, 2.705294, 2.707765, 2.710235, 2.712706, 2.715177, 2.717647, 2.720118, 2.722588, 2.725059, 2.72753, 2.73, 2.732471, 2.734941, 2.737412, 2.739882, 2.742353, 2.744824, 2.747294, 2.749765, 2.752235, 2.754706, 2.757794, 2.760882, 2.763971, 2.767059, 2.769118, 2.771177, 2.773235, 2.775294, 2.777353, 2.779412, 2.781882, 2.784353, 2.786824, 2.789294, 2.791765, 2.793824, 2.795882, 2.797941, 2.8, 2.802059, 2.804118, 2.807206, 2.810294, 2.813382, 2.816471, 2.81853, 2.820588, 2.822647, 2.824706, 2.826765, 2.828824, 2.830883, 2.832941, 2.835, 2.837059, 2.839118, 2.841177, 2.843647, 2.846118, 2.848588, 2.851059, 2.853529, 2.856, 2.858471, 2.860941, 2.863412, 2.865882, 2.867941, 2.87, 2.872059, 2.874118, 2.876177, 2.878235, 2.880294, 2.882353, 2.884412, 2.886471, 2.88853, 2.890588, 2.893059, 2.89553, 2.898, 2.900471, 2.902941, 2.905, 2.907059, 2.909118, 2.911177, 2.913235, 2.915294, 2.917059, 2.918824, 2.920588, 2.922353, 2.924118, 2.925883, 2.927647, 2.929412, 2.931177, 2.932941, 2.934706, 2.936471, 2.938235, 2.94, 2.942059, 2.944118, 2.946177, 2.948236, 2.950294, 2.952353, 2.953897, 2.955441, 2.956985, 2.958529, 2.960074, 2.961618, 2.963162, 2.964706, 2.966765, 2.968824, 2.970882, 2.972941, 2.975, 2.977059, 2.978824, 2.980588, 2.982353, 2.984118, 2.985882, 2.987647, 2.989412, 2.991471, 2.99353, 2.995588, 2.997647, 2.999706, 3.001765, 3.00353, 3.005294, 3.007059, 3.008824, 3.010588, 3.012353, 3.014118, 3.016177, 3.018235, 3.020294, 3.022353, 3.024412, 3.026471, 3.028235, 3.03, 3.031765, 3.03353, 3.035294, 3.037059, 3.038824, 3.040883, 3.042941, 3.045, 3.047059, 3.049118, 3.051177, 3.053236, 3.055294, 3.057353, 3.059412, 3.061471, 3.063529, 3.065074, 3.066618, 3.068162, 3.069706, 3.07125, 3.072794, 3.074338, 3.075882, 3.077941, 3.08, 3.082059, 3.084118, 3.086176, 3.088235, 3.08978, 3.091324, 3.092868, 3.094412, 3.095956, 3.0975, 3.099044, 3.100588, 3.102353, 3.104118, 3.105882, 3.107647, 3.109412, 3.111177, 3.112941, 3.115, 3.117059, 3.119118, 3.121177, 3.123235, 3.125294, 3.126838, 3.128382, 3.129927, 3.131471, 3.133015, 3.134559, 3.136103, 3.137647, 3.139412, 3.141177, 3.142941, 3.144706, 3.146471, 3.148236, 3.15, 3.15, 3.15, 3.15, 3.15]

NOM_RES = 10000
SER_RES = 9820
TEMP_NOM = 25
NUM_SAMPLES = 25
THERM_B_COEFF = 3950
ADC_MAX = 1023
ADC_Vmax = 3.15

class TempSensor:
    def __init__(self, pinNoTemp = 32)-> None:
        self.adc = ADC(Pin(pinNoTemp))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_10BIT)
        
    # Method to read the temperature from the thermistor
    # Time 13000 Microseconds
    def read_temp(self):
        raw_read = []
        # Collect NUM_SAMPLES
        for i in range(1, NUM_SAMPLES+1):
            raw_read.append(self.adc.read())

        # Average of the NUM_SAMPLES and look it up in the table after linearization
        raw_average = sum(raw_read)/NUM_SAMPLES
        #print('raw_avg = ' + str(raw_average))
        #print('V_measured = ' + str(adc_V_lookup[round(raw_average)]))

        # Convert the voltage to resistance
        raw_average = ADC_MAX * adc_V_lookup[round(raw_average)]/ADC_Vmax
        # print(raw_average)
        # print(len(adc_V_lookup))
        resistance = (SER_RES * raw_average) / (ADC_MAX - raw_average)
        # print('Thermistor resistance: {} ohms'.format(resistance))

        # Convert resistance to temperature
        steinhart  = -log(resistance / NOM_RES) / THERM_B_COEFF
        steinhart += 1.0 / (TEMP_NOM + 273.15)
        steinhart  = (1.0 / steinhart) - 273.15
        print('Temperature: {}°C'.format(steinhart))
        return steinhart
    
