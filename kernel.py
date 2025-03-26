import os

def process_input(user_input, context, active_afms):
    # ^response modifier
    if user_input.startswith("^"):
        modifier = user_input[1:].strip()
        print(f"[cidafm] Applying ^modifier: {modifier}")
        return {
            "afms": list(active_afms),
            "context": context,
            "user_input": f"^:{modifier}"
        }, context, active_afms

    # &state toggle
    elif user_input.startswith("&"):
        state = user_input[1:].strip()
        if state in active_afms:
            active_afms.remove(state)
            print(f"[cidafm] Toggled OFF: &{state}")
        else:
            active_afms.add(state)
            print(f"[cidafm] Toggled ON: &{state}")
        return {
            "afms": list(active_afms),
            "context": context,
            "user_input": None
        }, context, active_afms

    # !command
    elif user_input.startswith("!"):
        command = user_input[1:].strip()
        if command == "state-check":
            afm_list = "\n- " + "\n- ".join(sorted(active_afms)) if active_afms else "\n(None)"
            return {
                "afms": list(active_afms),
                "context": context,
                "user_input": f"[cidafm] Active AFMs:{afm_list}"
            }, context, active_afms
            
        if command.startswith("import-cid"):
            parts = command.split()
            if len(parts) != 2:
                return {
                    "afms": list(active_afms),
                    "context": context,
                    "user_input": "[cidafm] Usage: !import-cid filename"
                }, context, active_afms
            cid_path = parts[1]
            if not os.path.exists(cid_path):
                return {
                    "afms": list(active_afms),
                    "context": context,
                    "user_input": f"[cidafm] File not found: {cid_path}"
                }, context, active_afms
            with open(cid_path, "r") as f:
                lines = f.readlines()
            new_context = []
            afm_registry = {}
            current_section = None
            for line in lines:
                line = line.strip()
                if line == "[Context]":
                    current_section = "context"
                    continue
                elif line == "[AFMs]":
                    current_section = "afms"
                    continue
                elif not line:
                    continue

                if current_section == "context":
                    new_context.append(line)
                elif current_section == "afms":
                    if line[0] in "^&!":
                        parts = line.split(":", 1)
                        afm_type = line[0]
                        afm_name = parts[0][1:].strip()
                        afm_desc = parts[1].strip() if len(parts) > 1 else None
                        afm_registry[afm_name] = {
                            "type": {
                                "^": "response",
                                "&": "state",
                                "!": "command"
                            }[afm_type],
                            "description": afm_desc,
                            "active": afm_type == "&",
                            "source": cid_path
                        }
                    else:
                        print(f"[cidafm] Invalid AFM ignored: {line}")

            context.extend(new_context)
            active_afms.update({k for k, v in afm_registry.items() if v["type"] == "state" and v["active"]})
            print(f"[cidafm] Imported CID: {cid_path}")
            return {
                "afms": list(active_afms),
                "context": context,
                "user_input": f"CID imported: {cid_path}"
            }, context, active_afms

        else:
            return {
                "afms": list(active_afms),
                "context": context,
                "user_input": f"[cidafm] Unknown command: !{command}"
            }, context, active_afms

    # Normal user message
    else:
        return {
            "afms": list(active_afms),
            "context": context,
            "user_input": user_input.strip()
        }, context, active_afms