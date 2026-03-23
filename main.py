import os
import shutil
import xml.etree.ElementTree as ET


def extract_fritzing_images(fritzing_parts_dir, output_dir):
    print("🚀 Починаємо магію витягування картинок з Fritzing...")

    # Шляхи до папок всередині Fritzing
    core_fzp_dir = os.path.join(fritzing_parts_dir, 'core')
    svg_base_dir = os.path.join(fritzing_parts_dir, 'svg', 'core')

    # Створюємо папку images, якщо її ще немає
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(core_fzp_dir) or not os.path.exists(svg_base_dir):
        print(f"❌ Помилка: Не можу знайти папки Fritzing за шляхом: {fritzing_parts_dir}")
        print("Перевірте, чи правильно вказано шлях до папки 'fritzing-parts'!")
        return

    count = 0
    # Проходимося по всіх файлах деталей (.fzp - це XML файли з описом деталі)
    for fzp_file in os.listdir(core_fzp_dir):
        if not fzp_file.endswith('.fzp'):
            continue

        fzp_path = os.path.join(core_fzp_dir, fzp_file)
        try:
            tree = ET.parse(fzp_path)
            root = tree.getroot()

            # Отримуємо той самий ID, який ми використовували (moduleId)
            module_id = root.attrib.get('moduleId')

            # Шукаємо шлях до картинки для макетної плати (breadboardView)
            breadboard_view = root.find('.//breadboardView/layers')
            if breadboard_view is not None:
                image_path = breadboard_view.attrib.get('image')
                if image_path:
                    # Повний шлях до оригінальної SVG-картинки
                    src_svg_path = os.path.join(svg_base_dir, image_path)

                    # Якщо картинка фізично існує, копіюємо її
                    if os.path.exists(src_svg_path):
                        # Зберігаємо картинку під іменем її ID
                        dest_svg_path = os.path.join(output_dir, f"{module_id}.svg")
                        shutil.copy2(src_svg_path, dest_svg_path)
                        count += 1

        except Exception as e:
            # Ігноруємо пошкоджені файли, якщо такі є
            pass

    print(f"🎉 Успішно знайдено та скопійовано {count} картинок у форматі .svg!")
    print(f"📁 Всі файли знаходяться у папці: {output_dir}")


# --- НАЛАШТУВАННЯ ШЛЯХІВ ---

# ВКАЖІТЬ ТУТ ВАШ ШЛЯХ ДО ПАПКИ fritzing-parts (зверніть увагу на літеру r перед лапками)
FRITZING_PARTS_PATH = r"C:\Users\dmytr\Downloads\Fritzing  0.9.4.64\fritzing.0.9.4.64.pc\fritzing-parts"

# Куди зберегти картинки (папка images поруч зі скриптом)
OUTPUT_IMAGES_PATH = os.path.join(os.getcwd(), "images")

extract_fritzing_images(FRITZING_PARTS_PATH, OUTPUT_IMAGES_PATH)