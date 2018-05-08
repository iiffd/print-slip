import os.path

def delete_pdfs():
    ''' Deletes reports in downloads folder to save space '''
    packing_slips = []
    # Current working directory
    cwd = os.getcwd()
    for filename in os.listdir(cwd+'/packing_slips/'):
        if filename.endswith('.html') or filename.endswith('.pdf'):
            packing_slips.append(filename)
    # Deletes reports in Downloads
    for packing_slip in packing_slips:
        os.remove(cwd+'/packing_slips/' + packing_slip)
        print packing_slip, 'deleted'


if __name__ == '__main__':
    delete_pdfs()
