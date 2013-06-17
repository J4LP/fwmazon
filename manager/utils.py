import re
import json

from eve.models import InvType

class Fit():
    def to_json(self):
        final = {'ship': {}, 'modules': [], 'drones': []}
        final['ship']['ship_id'] = self.ship.id
        final['ship']['ship_name'] = self.ship.name
        final['ship']['fit_name'] = self.fit_name
        for m in self.modules:
            if hasattr(m, 'charge'):
                final['modules'].append({'id': m.id, 'name': m.name, 'charge_id': m.charge.id, 'charge_name': m.charge.name})
            else:
                final['modules'].append({'id': m.id, 'name': m.name})
        for d in self.drones:
            final['drones'].append({'id': d.id, 'name': d.name, 'amount': d.amount})
        return json.dumps(final)

    def import_eft(self, eft_string):
        offline_suffix = " /OFFLINE"
        eft_string = eft_string.strip()
        fit = {'modules': [], 'drones': []}
        lines = re.split('[\n\r]+', eft_string)
        info = lines[0][1:-1].split(",", 1)
        if len(info) == 2:
            shipType = info[0].strip()
            self.fit_name = info[1].strip()
        else:
            shipType = info[0].strip()
            self.fit_name = "Imported %s" % shipType

        try:
            self.ship = InvType.objects.get(name=shipType)
        except InvType.DoesNotExist:
            raise Exception('Parse Error')
            return


        drones = {}

        for i in range(1, len(lines)):
            line = lines[i]
            set_offline = line.endswith(offline_suffix)

            if set_offline == True:
                line = line[:len(line) - len(offline_suffix)]
            
            mod_ammo = line.split(",")
            mod_drone = mod_ammo[0].split(" x")

            if len(mod_ammo) == 2:
                ammo_name = mod_ammo[1].strip()
            else:
                ammo_name = None

            mod_name = mod_drone[0].strip()

            if len(mod_drone) == 2:
                drone_amount = mod_drone[1].strip()
            else:
                drone_amount = None

            try:
                item = InvType.objects.get(name=mod_name)
            except InvType.DoesNotExist:
                try:
                    item = InvType.objects.get(name=mod_ammo[0])
                    mod_name = mod_ammo[0]
                except:
                    continue
      
            if item.group.category.name == "Drone":
                drone_amount = int(drone_amount) if drone_amount is not None else 1
                
                if not mod_name in drones:
                    drones[mod_name] = 0
                drones[mod_name] += drone_amount
            else:
                if ammo_name:
                    try:
                        item.charge = InvType.objects.get(name=ammo_name)
                    except:
                        pass

                fit['modules'].append(item)

        for drone_name in drones:
            d = InvType.objects.get(name=drone_name)
            d.amount = drones[drone_name]
            fit['drones'].append(d)

        self.modules = fit['modules']
        self.drones = fit['drones']
        return self
