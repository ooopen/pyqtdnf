import mail1


class attachments:

    def items(self):
        return {[{'./bmp/back.bmp', 'file.bmp'}]}


a = {'./bmp/back.bmp': 'file.bmp'}

print(a.items())

#
mail1.send(subject='Test',
           text='This is a test!',
           recipients='375161864@qq.com',
           sender='1107769317@qq.com',
           username='1107769317@qq.com',
           password='mvbvvjyckktojegd',
           attachments={'file.bmp': './bmp/back.bmp'},
           smtp_host='smtp.qq.com')
