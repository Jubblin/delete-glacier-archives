import boto3
import json
from os.path import exists


def percentage(part, whole):
    import math
    percent = math.ceil(100 * float(part)/float(whole))
    return str(percent) + "%"


def counter_write(count, file):
    f = open(file, "w")
    f.write(str(count))
    f.close()


def counter_read(file):
    count = int(0)
    if exists(file):
        f = open(file, "r")
        count = int(f.read())
        counter_write(count, 'counter.startpoint.rec')
    return count


def delete_glacier_archive(vault, archive_id):
    session = boto3.Session()
    glacier = session.client('glacier')
    result = glacier.delete_archive(
        vaultName=vault_name,
        archiveId=archive_id
    )
    return result


json_source = "vault2.json"
count_file = "counter.rec"

place = counter_read(count_file)

# check for json json_source
if exists(json_source):
    with open(json_source, 'r') as json_file:
        json = json.load(json_file)
        vault_name = json['VaultARN'].split('/')[1]
        archive_count = len(json['ArchiveList'])
        counter = 0
        for arch in json['ArchiveList']:
            counter = counter + int(1)
            if counter > place:
                response = delete_glacier_archive(vault_name,arch['ArchiveId'])
                print('', end=f'\r Line: {str(counter)} of {str(archive_count)}, {percentage(counter, archive_count)}'
                              f' complete')
                counter_write(counter, count_file)

