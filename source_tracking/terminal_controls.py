from Controls import Rot2Prog
from Tracking import G2E , source_tracking





if __name__=='__main__':
    print('Welcome')

    control=Rot2Prog()
    conv=G2E()
    

    Switch=True

    while Switch:
        Input=input('')

        In=Input.split(' ')

        if In[0]=='P': #Pointing
        
            if len(In)==3:
                L=float(In[1])
                B=float(In[2])
                az,el=conv.Convert(L,B)
                az,el=int(az),int(el)
                if conv.Check_if_allowed_el(el):
                    control.point(az,el)
                    print(f'Pointing Toward ({L:.2f},{B:.2f})')
                else:
                    print(f'Not Valid Pointing for the Time and coordinate')

            else:
                print("Not Valid Entry... Try again")

        if In[0]=="Off": #Shutdown Telescope

            Switch=False

        if In[0]=='S': #slewing
            if len(In)==4: #with Az El Coordinates
                if In[-1]=='AzEl':
                    az=float(In[1])
                    el=float(In[2])
                    if conv.Check_if_allowed_el(el):
                        control.point(az,el)
                        print(f'Slewing Toward ({int(az)},{int(el)})')
                    else:
                        print(f'Not Valid Slew Pointing for the Time and coordinate')
                else:
                    print("Not Valid Entry... Try again")
                    
            elif len(In)==3: #with L B coordinates
                    L=float(In[1])
                    B=float(In[2])
                    az,el=conv.Convert(L,B)
                    az,el=int(az),int(el)
                    if conv.Check_if_allowed_el(el):
                        control.point(az,el)
                        print(f'Slewing Toward ({L:.2f},{B:.2f})')
                    else:
                        print(f'Not Valid Slew Pointing for the Time and coordinate')
            else:
                print("Not Valid Entry... Try again")
                    


        if In[0]=='R': # Restart
            control.Restart()
            
            
        else:
            print('Invalid Comand')

        Live=True

        if In[0]=='T':
                current_pointing=None
                if len(In)==3:
                    L=float(In[1])
                    B=float(In[2])
                    Source=source_tracking()
                    if current_pointing==None:
                        current_pointing=Source.pointing(L,B)
                    while Live:
                        

                        
                        
                    
                    
                    az,el=conv.Convert(L,B)
                    az,el=int(az),int(el)
                    if conv.Check_if_allowed_el(el):
                        control.point(az,el)
                        print(f'Pointing Toward ({L:.2f},{B:.2f})')
                    else:
                        print(f'Not Valid Pointing for the Time and coordinate')