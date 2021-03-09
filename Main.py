import os
import Dicom_convector_jpg as Dcj
import File_reader


def main():
    Output_Folder = 'Unet/data'
    template = 'masks'
    origin = 'imgs'

    if os.path.exists('logs.txt') is False:
        file = open('logs.txt', 'x')
        file.close()

    file_reader = File_reader.File_reader()
    start_number, Input_Image_List = file_reader.get_valid_path(['E:', 'D:/21.08.2020', 'D:/22.07.2020'])
    if os.path.isdir(Output_Folder + '/' + template) is False:
        os.mkdir(Output_Folder + '/' + template)
    if os.path.isdir(Output_Folder + '/' + origin) is False:
        os.mkdir(Output_Folder + '/' + origin)

    template_path = Output_Folder + '/' + template
    origin_path = Output_Folder + '/' + origin

    for i in range(start_number, len(Input_Image_List)):
        convector = Dcj.Dicom_convector_jpg(Input_Image_List[i], template_path, origin_path)
        convector.get_image(i)
        create_number_file = open('create_number.txt', 'w')
        create_number_file.write(str(i))
        create_number_file.close()

if __name__ == '__main__':
    main()
