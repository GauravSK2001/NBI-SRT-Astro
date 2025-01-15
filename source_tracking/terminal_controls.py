from Controls import Rot2Prog
from Tracking import G2E





if __name__=='__main__':
    print('Welcome')

    control=Rot2Prog()
    conv=G2E()
    

    Switch=True

    while Switch:
        Input=input('')

        In=Input.split(' ')

        if In[0]=='P':
            if len(In)==3:
                L=float(In[1])
                B=float(In[2])
                az,el=conv.Convert(L,B)
                if conv.Check_if_allowed_el(el):
                    control.point(az,el)
                    print(f'Pointing Toward ({int(L)},{int(B)})')
                else:
                    print(f'Not Valid Pointing for the Time and coordinate')

            else:
                print("Not Valid Entry... Try again")

        if In[0]=="Off":

            Switch=False

        else:
            print('Try Again, Invalid')

        
