from pathlib import Path
from tkinter import filedialog
import commands
import ttkbootstrap as ttk
from ttkbootstrap import Notebook
from ttkbootstrap.tableview import Tableview
import os



class App(ttk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Sqlite Viewer')
        self.iconbitmap('icon.ico')
        self.geometry('1000x800')
        self.db = None
        


        
        if not self.db:
            style = ttk.Style()
            style.configure('.', font=('Helvetica', 13))
            style.configure('info.Treeview', font=('roboto', 11), foreground='white', rowheight=30)
            
            style.configure('primary.Table.Treeview', font=('roboto', 10), rowheight=50)
            style.configure('primary.Table.Treeview.Heading', font=('roboto', 10))
            
            # style.configure('Scrollbar', heigth=100, background='black')
            self.change_file_button = ttk.Button(master=self, text='Change file', command=self.change_file)
            self.change_file_button.pack()
            self.choose_file()
            
    
    def choose_file(self):
        file  = filedialog.askopenfile(title='Choose a Sqlite file ')
        if file:
            end = Path(file.name).suffix # type: ignore
            if end in ['.db','.sdb','.sqlite','.db3','.s3db','.sqlite3','.sl3','.db2','.s2db','.sqlite2','.sl2']:
                self.db = file.name # type: ignore
                commands.db = self.db
                commands.start()
                self.run_app()

                return None
            else:
                # add warning
                return self.choose_file()
        else:
            return self.choose_file()
    def run_app(self):
        self.tab = Tabs()
        self.tab.pack(fill='both', expand=True)

        return 
    def change_file(self, *args, **kwargs):
        self = app
        self.tab.destroy()
        self.choose_file()
            
class TablesList(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tables = []
        self.heading('#0', text='Tables', anchor='w')
        self.column('#0', width=10000)
        
        

    def create_treeview(self):
        # add a scroll bar to the tables list to make viewing queries easy
        xscroll = ttk.Scrollbar(self, orient='horizontal')
        xscroll.config(command=self.xview)
        self.config(xscrollcommand=xscroll.set)
        xscroll.pack(side='bottom', fill='x')

        
        tables = commands.get_tables
        num = 0

        # get columns and sql query for a table in the db for the tables
        for table in tables:
            num +=1 
            col_id = self.gen_id()
            table_name,table_sql = table[1],table[4]
            self.insert('', num, col_id, text=f'{table_name}  ({table_sql})')
            rows = commands.get_rows(table_name)
            self.tables.append(table_name)

            for row in rows:

                row_id = self.gen_id()
                self.insert('',num+1, iid=row_id, text=row)
                self.move(row_id, col_id,num)
                num+=1
            
                
            
        return None
    def gen_id(self):
        from secrets import choice
        from string import hexdigits
        end = ''
        for i in range(10):
            end += choice(hexdigits)
        return end
    


class TableData(Tableview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.grid_columnconfigure(index=(1,10),pad=10)
    



    

class Tabs(Notebook):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # creates a list of all tables available
        self.table_view = TablesList(master=self, style='info.Treeview')
        self.table_view.create_treeview()
        self.table_view.place(relx=0, y=1, relwidth=0.20,relheight=1, bordermode='outside')
        
        # creates a frame for diaplying the data of a table
        self.browse = BrowseFrame(master=self)
        
        self.add(self.table_view, text=' Tables' )
        self.add(self.browse, text=' Browse Data ')
        self.bind('<<NotebookTabChanged>>', self.on_tab_change)

    def on_tab_change(self, *args, **kwargs):
        # wait till tab is changed till table is created
        if app.tab.focus_get() == app.tab.browse.dropdown:
            app.tab.browse.create_table()

        

class BrowseFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        


        self.tables = kwargs.get('master').table_view.tables # type: ignore
        self.default_table = self.tables[0]
        
        # dropdown menu for choosing table to display
        self.dropdown = ttk.Combobox(self, values=self.tables, width=50, state='readonly')
        self.dropdown.current(0)
        self.dropdown.bind('<<ComboboxSelected>>', self.change_table)
        self.dropdown.pack()

        self.table_with_data = None
        
        
    
    def change_table(self, *args, **kwargs):
        #  change current table being displays
        self = app.tab.browse
        table = self.dropdown.selection_get()
        self.default_table = table
        self.table_with_data.build_table_data(self.get_columns(), self.get_rows()) # type: ignore

    def create_table(self):
        # make tab wait until clicked before creating the table
        if self.table_with_data is None:
            self.table_with_data = TableData(master=self, stripecolor=('#003153', None), bootstyle='primary', coldata=self.get_columns(), rowdata=self.get_rows(), autoalign=True, autofit=True)
            self.table_with_data.pack(expand=True, fill='both')

        
    def get_columns(self):

        # get's and display the table names
        coldata = []

        for _table in commands.get_rows(self.default_table):
            col_data = {'text': _table, 'stretch':False}
            coldata.append(col_data)
        
        return coldata
    
    def get_rows(self):
        return commands.get_table_query(self.default_table)

if __name__ == '__main__':
    app = App(themename='superhero')
    app.mainloop()