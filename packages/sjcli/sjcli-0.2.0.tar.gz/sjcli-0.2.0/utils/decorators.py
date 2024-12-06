"""
Decorators to enchance functionality of default functions.
"""
def __print_formatter(function):
    def wrapper(message):
        print("-"*50)
        if type(message).__name__=="list":
            for msg in message:
                if type(msg).__name__=="tuple":
                    print(*msg,end="\n")
                elif type(msg).__name__=="str":
                    print(msg,end="\n")
        elif type(message).__name__=="tuple":
            print(*message,end="\n")
        else:
            print(message,end="\n")
        print("-"*50)
    return wrapper

@__print_formatter
def pprint(message):
    print(message)

if __name__=="__main__":
    lst=[(1, 'SQLite Database “CRUD Operations” using Python. | by Narendra Harny | Analytics Vidhya | Medium', 'https://medium.com/analytics-vidhya/sqlite-database-crud-operations-using-python-3774929eb799'), (2, 'CA PPM Release and Support Lifecycle Dates', 'https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/release-announcements/CA-PPM-Release-and-Support-Lifecycle-Dates/5894'), (3, 'Configuring HTTPS on Clarity', 'https://knowledge.broadcom.com/external/article?articleId=9783'), (4, 'Operation not permitted error while starting Clarity services', 'https://knowledge.broadcom.com/external/article/214504/operation-not-permitted-error-while-star.html'), (5, 'Create a Time Varying Attribute and Slice request', 'https://knowledge.broadcom.com/external/article/375684'), (6, 'Default user setting Unit of measure for new UX', 'https://knowledge.broadcom.com/external/article/200076')]
    pprint(lst)
    t=(1, 'SQLite Database “CRUD Operations” using Python. | by Narendra Harny | Analytics Vidhya | Medium', 'https://medium.com/analytics-vidhya/sqlite-database-crud-operations-using-python-3774929eb799')
    pprint(t)
    pprint("Saurabh")