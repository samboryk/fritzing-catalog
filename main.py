import os
import shutil
import xml.etree.ElementTree as ET


def extract_smart_images(fritzing_parts_dir, output_dir):
    print("search: Глибокий пошук з обробкою Generic IC...")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    svg_base_dir = os.path.join(fritzing_parts_dir, 'svg', 'core', 'breadboard')
    # Стандартний шаблон для мікросхем у Fritzing
    generic_ic_path = os.path.join(svg_base_dir, 'generic_ic_dip_8_pin_300mil_breadboard.svg')

    count = 0
    parts_dirs = [os.path.join(fritzing_parts_dir, d) for d in ['core', 'user', 'contrib']]

    for p_dir in parts_dirs:
        if not os.path.exists(p_dir): continue

        for fzp_file in os.listdir(p_dir):
            if not fzp_file.endswith('.fzp'): continue

            try:
                tree = ET.parse(os.path.join(p_dir, fzp_file))
                root = tree.getroot()
                module_id = root.attrib.get('moduleId')

                # Перевіряємо шлях до картинки
                layers = root.find('.//breadboardView/layers')
                if layers is not None:
                    img_name = layers.attrib.get('image')
                    # Шукаємо в папці svg/core/breadboard/
                    full_img_path = os.path.join(fritzing_parts_dir, 'svg', 'core', 'breadboard', img_name)

                    if os.path.exists(full_img_path):
                        shutil.copy2(full_img_path, os.path.join(output_dir, f"{module_id}.svg"))
                        count += 1
                    elif "generic_ic" in img_name or "prefix" in module_id:
                        # Якщо це Generic деталь - копіюємо хоча б стандартний вигляд мікросхеми
                        if os.path.exists(generic_ic_path):
                            shutil.copy2(generic_ic_path, os.path.join(output_dir, f"{module_id}.svg"))
                            count += 1
            except:
                continue

    print(f"Done! Витягнуто {count} картинок.")


# Вкажіть шлях
extract_smart_images(r"C:\Users\dmytr\Downloads\Fritzing  0.9.4.64\fritzing.0.9.4.64.pc\fritzing-parts", "images")