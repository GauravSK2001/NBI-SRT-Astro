import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from astropy import constants as const
from astropy.cosmology import Planck18 as planck18





class Atmospheric_effects:
    
    
    def __init__(self,air_temperature):
        self.optical_depth=3.4e-2 *np.log(10)/10 #optical depth of the atmosphere standard value
        self.air_temperature= air_temperature *u.K #temperature of the air in kelvin
        
    def slant_path_optical_depth(self,elevation_angle):
        theta= np.pi/2 - np.deg2rad(elevation_angle).value
        a=0.1500
        b=np.deg2rad(3.885).value
        c=1.253
        airmass=(np.sin(elevation_angle)-a*(elevation_angle+b)**(-c))**-1
        tau= self.optical_depth*airmass
        return tau
    
    def atmospheric_emission(self,elevation_angle):
        tau= self.slant_path_optical_depth(elevation_angle*u.deg)
        T= self.air_temperature*(1-np.exp(-tau))
        return T
    
    def atmospheric_absorption(self,elevation_angle,Observed_temperature):
        tau= self.slant_path_optical_depth(elevation_angle)
        T= Observed_temperature/(np.exp(-tau))
        return T

# Calibration class
class Calibration:
    '''
    Y method of calibration
    
    '''
    
    def __init__(self,calibration_integration_time,air_temperature):
        self.calibration_integration_time= calibration_integration_time *u.s
        self.air_temperature= air_temperature *u.K #temperature of the air in kelvin
        self.atmospheric= Atmospheric_effects(air_temperature)
        self.CMB_temperature= planck18.Tcmb0.to(u.K)
        self.Hot_temperature= 0
        self.Cold_temperature= 0
        self.slope= 0
        self.intercept= 0
        self.T_sys= 0
        self.T_cal = 0
    def cold_temperature(self,elevation_angle):
        
        T_cold= self.atmospheric.atmospheric_emission(elevation_angle) + self.CMB_temperature
        self.Cold_temperature= T_cold
        return T_cold
    
    def hot_temperature(self,Calibration_surface_temperature):
        
        T_hot= Calibration_surface_temperature *u.K
        self.Hot_temperature= T_hot
        
        return T_hot
    
    def Y_factor(self,Continuum_Hot,Continuum_Cold):
        return Continuum_Hot/Continuum_Cold
    
    def Tsys(self,Continuum_Hot,Continuum_Cold):
        
        Y= self.Y_factor(Continuum_Hot,Continuum_Cold)
        Tsys= (self.Hot_temperature-Y*self.Cold_temperature)/(Y-1)
        self.T_sys= Tsys
        return Tsys
    
    def Tcal(self,Power,Continuum_Hot,Continuum_Cold):
        
        m= (self.Hot_temperature-self.Cold_temperature)/(Continuum_Hot-Continuum_Cold)
        b= (-1*(Continuum_Hot/(Continuum_Hot-Continuum_Cold))*(self.Hot_temperature-self.Cold_temperature))+self.Hot_temperature
        
        Tcal= m*Power + b
        self.T_cal= Tcal
        return Tcal
    
    def initialize(self,Continuum_Hot,Continuum_Cold,power,elavation,Calibration_surface_temperature):
        t_h=self.hot_temperature(Calibration_surface_temperature)
        t_c=self.cold_temperature(elavation)
        y_factor=self.Y_factor(Continuum_Hot,Continuum_Cold)
        system_temp=self.Tsys(Continuum_Hot,Continuum_Cold)
        Calibrated_curve=self.Tcal(power,Continuum_Hot,Continuum_Cold)
        return Calibrated_curve
    
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