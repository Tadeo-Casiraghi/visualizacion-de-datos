from extractor import SheetExtractor
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

directory_path = 'datos_educacion/2022'
all_files = os.listdir(directory_path)

names = {}
for file in all_files:
    if '_tp_' in file or '_tdf_' in file:
        continue
    names[file.split('_')[1]] = os.path.join(directory_path, file)

plt.figure(figsize=(12, 8))

counter = 1
for name, path in names.items():

    print(name, counter)
    counter += 1
    excel_file = pd.ExcelFile(path)

    dataset = {}
    for sheet in range(3, len(excel_file.sheet_names)):
        test = SheetExtractor(path, sheet)
        data = test.get('males', 'universitario:completo', ponderated = True, ranged = True, start_from='25-29')
        dataset[test.name] = data

    df = pd.DataFrame(dataset)
    df = df.transpose()

    # Plot the heatmap
    # plt.figure(figsize=(12, 8))
    # sns.heatmap(df, cmap="YlGnBu", annot=True, fmt=".2f")
    # plt.title("Heatmap of Categories by Item and Number Range")
    # plt.xlabel("Item")
    # plt.ylabel("Number Range")


    average_per_number_range = df.mean(axis= 0)

    # plt.figure(figsize=(12, 8))
    plt.plot(average_per_number_range, label = name)

plt.legend()
plt.show()
