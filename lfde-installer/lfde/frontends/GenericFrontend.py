import sys

from Frontend import Frontend

class GenericFrontend(Frontend):

    #@abstract
    #def gui_set_element_active(self):

    #@abstract
    #def gui_load_page(self, page):

    #@abstract
    #def gui_get_object_value(self, name):

    #@abstract
    #def gui_set_object_value(self, name, value):



    def __init__(self, choices, backend):
        Frontend.__init__(self, backend)
        self.choices = choices

        self.pages = []
        self.current_page = 0
        self.previous_page = 0
        self.gui_page = None

        # initiate all the page classes to objects
        for page_class in self.page_classes:
            self.pages.append(page_class(self))


        # add all of the pages into the steps notebook
        self.steps = self.builder.get_object("steps")
        for page in self.pages:
            self.gui_load_page(page)
            page.load_page()

        self.set_page(0)


    def forward(self):
        # allow the page to hook the click
        if self.pages[self.current_page].hook_forward() == True:
            self.set_page(self.current_page + 1)


    def quit(self):
        # send all of our pages the unload
        for page in self.pages:
            page.unload_page()

        sys.exit(0)

    def back(self):
        self.set_page(self.current_page - 1)

    def skip(self):
        if self.previous_page < self.current_page:
            self.forward()
        else:
            self.back()



    def set_page(self, number):
        self.previous_page = self.current_page

        if number >= len(self.pages) - 1:
            self.gui_set_sensitive("btn_forward", False)
        else:
            self.gui_set_sensitive("btn_forward", True)

        if number == 0:
            self.gui_set_sensitive("btn_back", False)
        else:
            self.gui_set_sensitive("btn_back", True)

        if self.gui_page != None and self.current_page != number:
            self.gui_page.page_leave()

        #TODO: rename the gui_page variable.  it's not a good name
        self.gui_page = self.pages[number]
        self.gui_set_title(self.gui_page.title)
        self.gui_display_page(number)
        self.current_page = number
        self.gui_page.page_enter()

