import winreg
import datetime

int_to_type={
    winreg.REG_SZ:'-',
    winreg.REG_MULTI_SZ:'hex(7)',
    winreg.REG_EXPAND_SZ:'hex(2)',
    winreg.REG_DWORD:'dword',
    winreg.REG_DWORD_LITTLE_ENDIAN:'UNDEFINED',
    winreg.REG_DWORD_BIG_ENDIAN:'UNDEFINED',
    winreg.REG_BINARY:'hex',
    winreg.REG_LINK:'UNDEFINED',
    winreg.REG_FULL_RESOURCE_DESCRIPTOR:'UNDEFINED',
}

def parse_key(key):
    keys = list()
    try:
        idx = 0
        while True:
            sub_key = winreg.EnumKey(key, idx)
            keys.append(sub_key)
            idx += 1
    except OSError:
        pass

    values = list()
    try:
        idx = 0
        while True:
            value = winreg.EnumValue(key, idx)
            values.append(value)
            idx += 1
    except OSError:
        pass

    return keys, values


def query_identifier(root_key_pair, identifier):
    assert isinstance(root_key_pair, tuple)
    assert len(root_key_pair) == 2

    reg_queue = [('', root_key_pair[0], root_key_pair[1])]
    result_key_queue = list()
    result_value_queue = list()

    while len(reg_queue) != 0:
        grandfather_name, parent_name, parent_key = reg_queue.pop(0)

        batch_keys, batch_values = parse_key(parent_key)

        new_grandfather_name = '\\'.join((grandfather_name, parent_name))
        for key in batch_keys:
            if identifier in key.lower():
                key_path = '\\'.join((new_grandfather_name, key))
                result_key_queue.append(key_path)
                continue

            try:
                new_sub_key = winreg.OpenKey(parent_key, key, 0, winreg.KEY_READ)
                reg_queue.append((new_grandfather_name, key, new_sub_key))
            except Exception as e:
                print(str(e), grandfather_name, parent_name, key)


        for value in batch_values:
            if identifier in value[0].lower():
                result_value_queue.append((new_grandfather_name, value))

        winreg.CloseKey(parent_key)

    return result_key_queue, result_value_queue


def parse_version():
    #todo:: match OS version
    pass


def parse_key_result(key_queue):
    delete_queue = list()
    recovey_queue = list()
    for each in key_queue:
        delete_queue.append('[-' + each + ']\n\n')
        recovey_queue.append('[' + each + ']\n\n')

    return delete_queue, recovey_queue


def parse_value_result(value_queue):
    delete_queue = list()
    recovey_queue = list()
    for each in value_queue:
        delete_queue.append('[' + each[0] + ']\n' + '"' + each[1][0] + '"=-\n\n')

        data_type = int_to_type[each[1][2]]
        content = ''
        if data_type == '-':
            content = '"' + each[1][1] + '"'
        elif data_type == 'UNDEFINED':
            raise TypeError('does not support {}'.format(each[1][2]))
        else:
            content = data_type + ':' + str(each[1][2])
        recovey_queue.append('[' + each[0] + ']\n' + '"' + each[1][0] + '"=' + content + '\n\n')

    return delete_queue, recovey_queue


def write_to(file_path, key_queue, value_queue):
    with open(file_path, 'w', encoding='utf8') as fw:
        #todo:: match OS version
        fw.write('Windows Registry Editor Version 5.00\n\n')

        for line in key_queue:
            fw.write(line)

        for line in value_queue:
            fw.write(line)


def query(identifier):
    classical_key = [
        ('HKEY_CLASSES_ROOT', winreg.HKEY_CLASSES_ROOT),
        ('HKEY_CURRENT_USER', winreg.HKEY_CURRENT_USER),
        ('HKEY_LOCAL_MACHINE', winreg.HKEY_LOCAL_MACHINE),
        #  ('HKEY_PERFORMANCE_DATA', winreg.HKEY_PERFORMANCE_DATA),
        #  ('HKEY_CURRENT_CONFIG', winreg.HKEY_CURRENT_CONFIG),
        #  ('HKEY_DYN_DATA', winreg.HKEY_DYN_DATA)
    ]

    key_queue = list()
    value_queue = list()
    for idx, each_key in enumerate(classical_key):
        print('{}/{}'.format(idx + 1, len(classical_key)), end='\t')

        batch_key_queue, batch_value_queue = query_identifier(each_key, identifier)
        key_queue.extend(batch_key_queue)
        value_queue.extend(batch_value_queue)

    delete_key, recovery_key = parse_key_result(key_queue)
    delete_value, recovery_value = parse_value_result(value_queue)

    postfix = datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S') + '.reg'
    delete_file_path = 'PyRegistry_' + 'delete_' + postfix
    recovery_file_path = 'PyRegistry_' + 'recovery_' + postfix

    write_to(delete_file_path, delete_key, delete_value)
    write_to(recovery_file_path, recovery_key, recovery_value)
