import yaml
import sys
from urllib.parse import urlsplit

def get_section(section):
    if 'show' in section and section['show'] == False:
        return 
    sec = f"\\section{{{section['title']}}}\n"
    if section['layout'] == 'list':
        sec += "\\resumeSubHeadingListStart\n"
        for item in section['content']:
            if 'show' in item and item['show'] == False:
                continue

            subheading = r"""\resumeSubheading
    {%s}{%s}
    {%s}{%s}
"""
            subheading_notitle = r"""\resumeSubheadingNoTitle
    {%s}{%s}
"""
            if 'sub_title' in item:
                sec += subheading % (item['title'], item['location'], item['sub_title'], item['duration'])
            else:
                if 'location' not in item:
                    item['location'] = ''
                sec += subheading_notitle % (item['title'], item['location'])
            desc = ""
            if 'description' in item:
                desc += "\\resumeItemListStart\n"
                for i in item['description']:
                    desc += "\t\\resumeItemOne{%s}\n" % (i)
                desc += "\\resumeItemListEnd\n"
            sec += desc
        sec += "\\resumeSubHeadingListEnd\n\n"
    elif section['layout'] == 'text':
        for line in section['content']:
            (key, value), = line.items()
            sec += f'{key}: {value}\\\\ \n'
    else:
        raise Exception("No 'layout' in the section.")
    return f'{sec}\n\n'

def get_heading(conf):
    heading = r"""\textbf{\href{%s}{\Large {%s}}} \\
{
    \href{mailto:{%s}}{{%s}} $|$ \href{%s}{%s} $|$ \href{tel:%s}{%s}
}
"""


    website = conf['website']
    url = urlsplit(website)
    website_path = None
    if url.path == '/':
        website_path = url.netloc
    else:
        website_path = url.netloc + url.path
    name = conf['name']
    email = conf['email']
    phone = conf['phone']
    return heading % (website, name, email, email, website, website_path, phone, phone)

def to_tex(conf):
    tex = ""
    with open("preamble.tex", "r") as f:
        tex = f.read()
    
    tex += get_heading(conf)
    if 'order' in conf:
        section_dict = {}
        for section in conf['content']:
            section_dict[section['title']] = section
        for sec_name in conf['order']:
            tex += get_section(section_dict[sec_name])
    else: 
        for section in conf['content']:
            tex += get_section(section)
    tex += r"\end{document}"
    return tex

def main():
    src_filename = sys.argv[1]

    if "yml" not in src_filename: 
        print(f"Please enter source yaml file with .yml or .yaml instead of {src_filename}")
        exit(1)

    dst_filename = None
    if len(sys.argv) == 3:
        dst_filename = sys.argv[2] 
    if dst_filename is not None and "tex" not in dst_filename: 
        print(f"Please enter destination tex file with .tex instead of {dst_filename}")
        exit(1)

    conf = None
    with open(src_filename, "r") as f:
        s = f.read()
        conf = yaml.load(s, yaml.FullLoader)
    
    tex = to_tex(conf)

    if dst_filename:
        f = open(dst_filename, "w")
        f.write(tex)
        f.close()
    else:
        print(tex)

if __name__ == "__main__":
    main()