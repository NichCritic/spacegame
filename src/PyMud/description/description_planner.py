"names" "material" "avatar_type" "actions" "close_to" "container" "surface" "open_container" "holding"


subset_fns = {
	"names": {"group_fn":lambda n:n.names.name if n.has('names') else ""},
	"material": {"group_fn":lambda n:n.material.material_id if n.has('material') else -1},
	"avatar_type": {"group_fn":lambda n: 1 if n.has('avatar_type') else 0},
	"actions": {"group_fn":lambda n:n.actions.action if n.has('actions') else ""},
	"close_to": {"group_fn":lambda n:n.close_to.n_id if n.has('close_to') else ""},
}


def get_subsets(node_list, available_keys):
	subsets = {}
	for k in available_keys:
		# print(k)
		ss =node_list.group_by(subset_fns[k]['group_fn'])
		# print(ss)
		subsets[k] = ss
	return subsets

def get_best_subset(subsets):
	best = -1000
	
	for k, subset in subsets.items():
		test = sum([len(s) ** 2 for s in subset.values()]) if len(subset) > 1 else -10000
		# print(test)
		# print("key: {}, subset:{}".format(k, subset))
		#import pdb;pdb.set_trace()
		if test > best or best == -1000:
			best = test
			res = subset
			key = k
	return key, res

def subdivide(node_list, available_keys):
	print([n.id for n in node_list])
	ret = []
	subsets = get_subsets(node_list, available_keys)
	best_key, best = get_best_subset(subsets)
	new_keys = available_keys[:]
	new_keys.remove(best_key)
	if len(new_keys) == 0 or len(best) == 1:
		return best_key, list(best.values())

	print(best_key, best)
	import pdb;pdb.set_trace()

	for k, s in best.items():
		if len(s) > 1:
			ret.append(subdivide(s, new_keys))
		else:
			ret.append(s)
	return best_key, ret



