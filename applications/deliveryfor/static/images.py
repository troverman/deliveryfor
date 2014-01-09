#######################################################################
#######################################################################
#######################################################################
 
class RESIZE(object):
    def __init__(self, nx=160, ny=80, error_message=' image resize'):
        (self.nx, self.ny, self.error_message) = (nx, ny, error_message)
     
    def __call__(self, value):
        if isinstance(value, str) and len(value) == 0:
            return (value, None)
        
        from PIL import Image
        import cStringIO
        try:
            img = Image.open(value.file)
            img.thumbnail((self.nx, self.ny), Image.ANTIALIAS)
            s = cStringIO.StringIO()
            img.save(s, 'JPEG', quality=100)
            s.seek(0)
            value.file = s
        except:
            return (value, self.error_message)
        else:
            return (value, None)
 
def THUMB(image, nx=120, ny=120, gae=False, name='thumb'):
    if image:
        if not gae:
            request = current.request
            from PIL import Image
            import os
            img = Image.open(request.folder + 'uploads/' + image)
            img.thumbnail((nx, ny), Image.ANTIALIAS)
            root, ext = os.path.splitext(image)
            thumb = '%s_%s%s' % (root, name, ext)
            img.save(request.folder + 'uploads/' + thumb)
            return thumb
        else:
            return image
