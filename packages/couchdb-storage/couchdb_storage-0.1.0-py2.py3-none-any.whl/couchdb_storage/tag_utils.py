from .file_db import FileDb


def interact_with_user_for_tagging_path(full_path, default_tag_str=""):
    d = FileDb()
    taggable_obj = d.get_file_obj_for_path(full_path)
    if len(taggable_obj.get_tags()) != 0:
        current_tags = taggable_obj.get_tags()
        print(f"current tags: {current_tags}")
    else:
        print(f"{full_path} is not tagged yet")

    prompt = 'Please enter more tags separated by comma'
    if default_tag_str != "":
        prompt += f", if nothing is entered \"{default_tag_str}\" will be used:"
    else:
        prompt += ":"

    input_tags_str = input(prompt)
    if input_tags_str == "":
        if default_tag_str != "":
            input_tags_str = default_tag_str
            print(f"No tag entered, use \"{input_tags_str}\"")
        else:
            print("No tag entered, return")
            return
    taggable_obj.append_tags([s.strip() for s in input_tags_str.split(',')])
    taggable_obj.save()
    return input_tags_str

