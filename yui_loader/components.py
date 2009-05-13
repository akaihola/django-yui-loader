class ComponentAdapter:

    def __init__(self, components, name, data):
        self.components = components
        self.name = name
        self.data = data

    @property
    def optional(self):
        return self.data.get('optional', [])

    @property
    def supersedes(self):
        return self.data.get('supersedes', [])

    @property
    def requires(self):
        r = self.data.get('requires', [])

        if self.type != 'js' \
        or self.name == 'yahoo' \
        or 'yahoo' in self.supersedes \
        or 'yahoo' in r:
            return r
        else:
            return ['yahoo'] + r

    @property
    def after(self):
        if self.type == 'css':
            return self.data.get('after', [])
        elif self.type == 'js':
            return self.data.get('after', []) + \
                   self.components.get_css_components()

    @property
    def rollup(self):
        return self.data.get('rollup', 1)

    @property
    def skinnable(self):
        return self.data.get('skinnable', False)

    @property
    def fullpath(self):
        return self.data.get('fullpath', None)

    def __getattr__(self, attname):
        return self.data[attname]


class Components(dict):
    def __init__(self, components_dict):
        super(Components, self).__init__()
        self.rollup_mapping = {}
        for component_name, data in components_dict.items():
            self.add(component_name, data)

    def __getitem__(self, component_name):
        data = super(Components, self).__getitem__(component_name)
        return ComponentAdapter(self, component_name, data)

    def get_rollups(self, component_name):
        return self.rollup_mapping[component_name]

    def get_all_rollups(self, component_name):
        rollups = self.get_rollups(component_name)
        for superseded in self[component_name].supersedes:
            rollups.update(self.get_all_rollups(superseded))
        return rollups

    def get_css_components(self):
        return [name for name, data in self.items()
                if data['type'] == 'css']

    def add(self, component_name, data):
        self[component_name] = data
        self.rollup_mapping.setdefault(component_name, set())
        if 'rollup' not in data:
            return
        for rolled_up in data['supersedes']:
            self.rollup_mapping.setdefault(rolled_up, set()).add(
                component_name)
