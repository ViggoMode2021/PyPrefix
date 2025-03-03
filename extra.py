potential_subnets = []

        try:
            for x in range(main_mask, 33): # Enumerate parent loop with subnet mask lengths that range from main mask to 32.
                for i in ipaddress.ip_network(subnet).subnets(new_prefix=x): # Find all potential subnets in main subnet
                    potential_subnets.append(i)
            potential_subnets_total = len(potential_subnets)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"\nThere are a total of {potential_subnets_total} potential subnets within supernet of {subnet}.")
        except ValueError:
            print(f"Cannot generate list of potential subnets encapsulated in {subnet}.")
