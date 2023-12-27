from jinja2 import Environment, FileSystemLoader
import yaml

def config_generator_from_excel_upe2(excel_filename):

    upe2_yaml_filename = "/var/www/html/ne80_config_generator/upe2-temp.yml"
    variables = {}
    upe2_list = []

    with open(excel_filename, "r") as excel_csv:
        for line in excel_csv:
            upe2_list.append(line.strip().split(';'))

        for element in upe2_list[28:]:
            key = element[0].strip()
            value = element[1].strip()

            #X2_vrf icin tek haneli plaka kodlarina "0" eklemek icin ..
            if key == "PLAKA_KOD" and len(value) < 2:
                value = "0" + value
                
            variables[key] = value

    with open(upe2_yaml_filename, "w+") as yf :
        yf.write("-")
        count = 0
        for k,v in variables.items():
            if count == 0:
                yf.write(f" {k} : {v} \n")
            else:
                yf.write(f"  {k} : {v} \n")
            count +=1

    #env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
    env = Environment(loader=FileSystemLoader('/var/www/html/ne80_config_generator/templates'))
    template = env.get_template('template-upe2.j2')

    with open('/var/www/html/ne80_config_generator/upe2-temp.yml') as f:
        routers = yaml.safe_load(f)

    for router in routers:
        r1_conf = router['HOSTNAME'] + '.txt'
        with open(f"/var/www/html/ne80_config_generator/konfigs/{r1_conf}", 'w') as f:
            f.write(template.render(router))
            out = (template.render(router))

    return out
