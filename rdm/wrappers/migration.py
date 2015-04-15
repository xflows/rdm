
for w in AbstractWidget.objects.filter(package='ilp'):
    w.package = 'rdm.wrappers'
    w.save()
