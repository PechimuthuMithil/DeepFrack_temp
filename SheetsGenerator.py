import os
import yaml
import json
import csv

def Read(stats_file):
    stats_file = stats_file+'/timeloop-mapper.stats.txt'
    with open(stats_file, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip() == "Summary Stats":
            # Read pJ/Compute
            pJ_compute_line = lines[i+24].strip()
            pJ_compute = float(pJ_compute_line.split('=')[1].strip())

            # Read Computes
            computes_line = lines[i+9].strip()
            computes = int(computes_line.split('=')[1].strip())

            # Read Cycles
            cycles_line = lines[i+4].strip()
            cycles = int(cycles_line.split(':')[1].strip())
            # Add to summary_stats dictionary

        if line.strip() == "pJ/Compute":
            # For Eyeriss
            mac = float(lines[i+1].strip().split('=')[1].strip())
            psum_spad = float(lines[i+2].strip().split('=')[1].strip())
            weights_spad = float(lines[i+3].strip().split('=')[1].strip())
            ifmap_spad = float(lines[i+4].strip().split('=')[1].strip())
            DummyBuffer = float(lines[i+5].strip().split('=')[1].strip())
            shared_glb = float(lines[i+6].strip().split('=')[1].strip())
            DRAM = float(lines[i+7].strip().split('=')[1].strip())

    # LatencyPerCompute = cycles/computes
    return [cycles,mac,psum_spad,weights_spad,ifmap_spad,DummyBuffer,shared_glb,DRAM,computes]

def load_dictionary_from_file(filename):
    with open(filename, 'r') as file:
        dictionary = json.load(file)
    return dictionary

def GetNum(FileName):
    num = int(FileName[-7:-5])
    return num

def write_to_csv(file_path, data_list):
    try:
        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header if needed
            # writer.writerow(['Column1', 'Column2', 'Column3'])
            for data_row in data_list:
                writer.writerow(data_row)
        print(f"Data successfully written to {file_path}")
    except IOError:
        print(f"Error writing to {file_path}")

layers = []

layer_folder_path = '/workspace/WrapperTest/ExperimentVGG/VGG02'  # Please note that the layers should be named 01,02,03...
file_path = "/workspace/dataDATE.csv" # Path to csv file
LogFile_filder_path = '' # Path to the folder that contains the Log Files created during the Bench Marking process

for file_name in os.listdir(layer_folder_path):
    if file_name.endswith('.yaml'):
        file_path = os.path.join(layer_folder_path, file_name)
        layers.append(file_path)
layers.sort(key = GetNum)

stacks = [(0,7),(8,9),(10,10),(11,12)] # Get these vales from the Stats File from the DeepFrack Wrapper
tiles = [7,4,14,4] # Get these vales from the Stats File from the DeepFrack Wrapper
WCPs = ['11111110','11','0','11'] # Get these vales from the Stats File from the DeepFrack Wrapper

datata = []

### TO GET WHAT IS THE TILES AVAILABLE ###
LBLCFile = '/workspace/WrapperTest/ExperimentVGG/LBLCUpdated.json'
LBLC = load_dictionary_from_file(LBLCFile)

for k in range(len(stacks)):
    stack = stacks[k]  # tuple of index in layers
    WCP = WCPs[k]
    tile_size = tiles[k]
    ### OUTPUTS ###
    Latency = 0
    pJCompute_LMAC = 0
    pJCompute_psum_spad = 0
    pJCompute_weight_spad = 0
    pJCompute_ifmap_spad = 0
    pJCompute_DummyBuffer = 0
    pJCompute_shared_glb = 0
    pJCompute_DRAM = 0
    TotalEnergy = 0
    TotalComputes = 0


    n = len(layers)
    count = stack[1]-stack[0]
    if (stack[0] == stack[1]):
        layer = stack[1]
        stats_file = LogFile_filder_path +f'/LogFiles/SLC/Layer{stacks[0]+1}/tile_size'
        data = Read(stats_file)
        Latency += data[0]
        pJCompute_LMAC += data[1]*data[8]
        pJCompute_psum_spad += data[2]*data[8]
        pJCompute_weight_spad += data[3]*data[8]
        pJCompute_ifmap_spad += data[4]*data[8]
        pJCompute_DummyBuffer += data[5]*data[8]
        pJCompute_shared_glb += data[6]*data[8]
        pJCompute_DRAM += data[7]*data[8]
        TotalComputes += data[8]
    else:
        for layer in range(stack[1],stack[0]-1,-1):
            prob = layers[layer]
            while (str(tile_size) not in LBLC[str(layer+1)]):
                tile_size -= 1
            if (layer == stack[1]):
                if (WCP[count] == '0'):
                    stats_file = LogFile_filder_path +f'/LogFiles/Start/Layer{stacks[0]+1}/tile_size'
                    data = Read(stats_file)
                else:
                    stats_file = LogFile_filder_path +f'/LogFiles/OutWCC/Layer{stacks[0]+1}/tile_size'
                    data = Read(stats_file)   
            elif (layer == stack[0]):
                if (WCP[count] == '0'):
                    stats_file = LogFile_filder_path +f'/LogFiles/ELBLC/Layer{stacks[0]+1}/tile_size'
                    data = Read(stats_file)
                else:
                    stats_file = LogFile_filder_path +f'/LogFiles/EWCC/Layer{stacks[0]+1}/tile_size'
                    data = Read(stats_file)
            else:
                if (WCP[count] == '0'):
                    stats_file = LogFile_filder_path +f'/LogFiles/LBLC/Layer{stacks[0]+1}/tile_size'
                    data = Read(stats_file)
                else:
                    stats_file = LogFile_filder_path +f'/LogFiles/WCC/Layer{stacks[0]+1}/tile_size'
                    data = Read(stats_file) 
            count -= 1
            Latency += data[0]
            pJCompute_LMAC += data[1]*data[8]
            pJCompute_psum_spad += data[2]*data[8]
            pJCompute_weight_spad += data[3]*data[8]
            pJCompute_ifmap_spad += data[4]*data[8]
            pJCompute_DummyBuffer += data[5]*data[8]
            pJCompute_shared_glb += data[6]*data[8]
            pJCompute_DRAM += data[7]*data[8]
            TotalComputes += data[8]
            with open(prob, 'r') as file:
                    data = yaml.safe_load(file)

            # Output Dimensions:
            for data_space in data['problem']['shape']['data-spaces']:
                '''
                In the next few lines we are extracting the dimension from the workload YAML file
                '''
                if (data_space['name'] == 'Inputs'):
                    for dim in data_space['projection']:
                        if len(dim) == 2:
                            for i in dim:
                                if (i[1] == 'Wdilation'):
                                    Kernel_Width = data['problem']['instance'][i[0]]
                                    Wdilation = data['problem']['instance']['Wdilation']
                                elif (i[1] == 'Wstride'):
                                    Output_Width = data['problem']['instance'][i[0]]
                                    Wstride = data['problem']['instance']['Wstride']
                                elif (i[1] == 'Hdilation'):
                                    Kernel_Height = data['problem']['instance'][i[0]]
                                    Hdilation = data['problem']['instance']['Hdilation']
                                elif (i[1] == 'Hstride'):
                                    Output_Height = data['problem']['instance'][i[0]]
                                    Hstride = data['problem']['instance']['Hstride']
            Padding_Width = 0
            tile_size = ((tile_size - 1) * Wstride) - (2 * Padding_Width) + (Wdilation * (Kernel_Width - 1)) + 1

    datata.append([pJCompute_LMAC/TotalComputes, pJCompute_psum_spad/TotalComputes,pJCompute_weight_spad/TotalComputes, pJCompute_ifmap_spad/TotalComputes,pJCompute_DummyBuffer/TotalComputes,pJCompute_shared_glb/TotalComputes,pJCompute_DRAM/TotalComputes,Latency,TotalComputes])

    print('Latency:',Latency)
    print('pJmac:',pJCompute_LMAC/TotalComputes)
    print('pJCompute_psum_spad:',pJCompute_psum_spad/TotalComputes)
    print('pJCompute_weight_spad:',pJCompute_weight_spad/TotalComputes)
    print('pJCompute_ifmap_spad:',pJCompute_ifmap_spad/TotalComputes)
    print('pJCompute_DummyBuffer:',pJCompute_DummyBuffer/TotalComputes)
    print('pJCompute_shared_glb:',pJCompute_shared_glb/TotalComputes)
    print('pJCompute_DRAM:',pJCompute_DRAM/TotalComputes)
    print('TotalComputes:',TotalComputes)    
    
data_to_write = datata
write_to_csv(file_path, data_to_write)