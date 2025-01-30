import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from astropy import constants as const
from astropy.cosmology import Plack18 as planck18





class Atmospheric_effects:
    
    
    def __init__(self,air_temperature):
        self.optical_depth=0.005 #optical depth of the atmosphere standard value
        self.air_temperature= air_temperature #temperature of the air in kelvin
        
    def slant_path_optical_depth(self,elavation_angle):
        theta= np.pi/2 -np.deg2rad(elavation_angle)
        tau= self.optical_depth/np.cos(theta)
        return tau
    
    def atmospheric_emission(self,elavation_angle):
        tau= self.Slant_path_optical_depth(elavation_angle)
        T= self.air_temperature*(1-np.exp(-tau))
        return T
    
    def atmospheric_absorption(self,elavation_angle,Observed_temperature):
        tau= self.slant_path_optical_depth(elavation_angle)
        T= Observed_temperature/(np.exp(-tau))
        return T

# Calibration class
class Calibration:
    '''
    Y method of calibration
    
    '''
    
    def __init__(self,calibration_intigration_time,air_temperature):
        self.calibration_intigration_time= calibration_intigration_time
        self.air_temperature= air_temperature #temperature of the air in kelvin
        self.atmospheric= Atmospheric_effects(air_temperature)
        self.CMB_temperature= planck18.Tcmb0.to(u.K)
        self.Hot_temperature= 0
        self.Cold_temperature= 0
        self.slope= 0
        self.intercept= 0
        self.Tsys= 0
    def cold_temperature(self,elavation_angle):
        
        T_cold= self.atmospheric.atmospheric_emission(elavation_angle) + self.CMB_temperature
        self.Cold_temperature= T_cold
        return T_cold
    
    def Hot_temperature(self,Calibration_surface_temperature):
        
        T_hot= Calibration_surface_temperature
        self.Hot_temperature= T_hot
        
        return T_hot
    
    def Y_factor(self,Continuum_Hot,Continuum_Cold):
        return Continuum_Hot/Continuum_Cold
    
    def Tsys(self,Continuum_Hot,Continuum_Cold):
        
        Y= self.Y_factor(Continuum_Hot,Continuum_Cold)
        Tsys= (self.Hot_temperature-Y*self.Cold_temperature)/(Y-1)
        return Tsys
    
    def Tcal(self,Power,Continuum_Hot,Continuum_Cold):
        
        m= (self.Hot_temperature-self.Cold_temperature)/(Continuum_Hot-Continuum_Cold)
        b= (-1*(Continuum_Hot/(Continuum_Hot-Continuum_Cold))*(self.Hot_temperature-self.Cold_temperature))+self.Hot_temperature
        
        Tcal= m*Power + b
        return Tcal
    
    def Plotter(self):
        '''
        TO DO: 
        1. add the Tcold and Thot to the plot
        2. add the Tsys to the plot
        
        '''
        x= np.linspace(0,self.Hot_temperature+10,100)
        y= self.slope*x + self.intercept
        fig, ax = plt.subplots()
        ax.plot(x,y)
        
        ax.set(xlabel=r'Power ($P$)', ylabel=r'Temperature ($T$) [K]',title='Calibration')
        ax.grid()
        plt.show()