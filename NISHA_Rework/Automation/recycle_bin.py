import winshell

#Nisha check all items in recycle bin
for item in winshell.recycle_bin(): #Nisha check all items in recycle bin
    print(f'{item}')


#Restore a particular file
def restore_a_file(FILE_NAME):
    '''Restore a particular file'''
    for item in winshell.recycle_bin():
        if "filename To NISHA" in item.original_filename():
            winshell.undelete(item.original_filename())
            break

#
def empty_recycle_bin(bool):
    '''Empty Recycle Bin'''
    winshell.empty_recycle_bin()


