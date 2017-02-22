# PERMISSIONS DATA STRUCTURE
class Permissions:
    UNLOCK = 0x01       #Unlock node
    LOCK = 0x02         #lock node
    DAT = 0x04          #Default access time frame
    OVERRIDE_UAT = 0x08 #Can define
    ADD_USER = 0x0F
    REMOVE_USER = 0x20
    OVERRIDE_DAT = 0x40
    NAME = 0x80
    IP_ADDRESS = 0x100
    ONLINE = 0x200

    STANDARD = UNLOCK | LOCK | DAT
    SUPER = STANDARD | OVERRIDE_UAT | ADD_USER | REMOVE_USER | OVERRIDE_DAT
    ADMIN = SUPER | NAME | IP_ADDRESS | ONLINE

    permission_dict = {'UNLOCK': UNLOCK, 'LOCK': LOCK, 'DAT': DAT, 'OVERRIDE_UAT': OVERRIDE_UAT,
                  'ADD_USER': ADD_USER, 'REMOVE_USER': REMOVE_USER, 'OVERRIDE_DAT': OVERRIDE_DAT,
                  'NAME': NAME, 'IP_ADDRESS': IP_ADDRESS, 'ONLINE': ONLINE, 'STANDARD': STANDARD,
                       'SUPER': SUPER, 'ADMIN': ADMIN}
    roll = ''
    def build_permissions(self, form_input):
        try:
            return self.permission_dict[form_input]
        except KeyError:
            return False

data = 'ADMIN'
try:
    print(Permissions.permission_dict[data])
except KeyError:
    print('Error')

