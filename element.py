class element(object):
    def __init__(self, hier):
        self.visible = hier['visible-to-user']
        self.clickable = hier['clickable']
        self.bounds = hier['bounds']
        self.name = hier['class'].split('.')[-1]
        self.full_name = hier['class']
        self.scrollable = {'horizontal': hier['scrollable-horizontal'],
                           'vertical': hier['scrollable-vertical']}
        self.resource_id = hier['resource-id'].split('/')[-1] if 'resource-id' in hier else None
        self.text = hier['text'] if 'text' in hier else None
        self.children = [element(i) for i in hier['children']] if 'children' in hier else None

        # Exception postprocess
        # - if children is invisible, delete it
        wait_del = list()
        if self.children is not None:
            for child in self.children:
                if not child.visible:
                    wait_del.append(child)

        for it in wait_del:
            self.children.remove(it)

        # Exception postprocess
        # - if DrawerLayout has 2+ layout/views (which means, drawer has opened),
        #   delete original layout/view (which priors to the drawer view)
        if self.name.count("DrawerLayout") and len(self.children) > 1:
            self.children.remove(self.children[0])

        # Exception postprocess
        # - if SlidingMenu has 2+ layout/views (which means, slide has opened),
        #   delete original layout/view (which priors to the slide view)
        if self.name == "SlidingMenu" and len(self.children) > 1:
            self.children.remove(self.children[1])

        # Exception postprocess
        # - if element's width/height is under 0 (which is confusing),
        #   delete the element
        if self.children is not None:
            for child in self.children:
                if (child.bounds[2] - child.bounds[0]) < 0 or (child.bounds[3] - child.bounds[1]) < 0:
                    self.children.remove(child)

        # Exception postprocess
        # - if FanView has 2+ layout/views (which means, fan has opened),
        #   delete original layout/view (which priors to the slide view)
        if self.name == "FanView" and len(self.children[0].children) > 1:
            self.children[0].children = [self.children[0].children[0]]

    def __str__(self):
        out = '{' \
              + ("visible: %s, " % self.visible) \
              + ("clickable: %s, " % self.clickable) \
              + ("bounds: %s, " % self.bounds) \
              + ("name: '%s', " % self.name) \
              + ("full_name: '%s', " % self.full_name) \
              + ("scrollable: %s, " % self.scrollable) \
              + ("resource_id: %s, " % ("'" + self.resource_id + "'" if self.resource_id is not None else "None")) \
              + ("text: %s" % ("'" + self.text + "'" if self.text is not None else "None")) \
              + ("children: %s" % self.children) \
              + '}'

        return out

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        out = {'visible': self.visible,
               'clickable': self.clickable,
               'bounds': self.bounds,
               'name': self.name,
               'full_name': self.full_name,
               'scrollable': self.scrollable,
               'resource_id': self.resource_id,
               'text': self.text,
               'children': [child.to_dict() for child in self.children] if self.children is not None else None}

        return out
