def prune_json(j, selected_keys):
                prunned_json = {x: j[x] for x in selected_keys if x in j}                
                return prunned_json