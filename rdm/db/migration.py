
for w in AbstractWidget.objects.filter(package='mysql'):
    w.package='rdm.db'
    w.save()
