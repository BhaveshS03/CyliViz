import math
class Mapper:
    @staticmethod
    def mapper(colormap,values):
        # --- Processing ---
        simplified_cmap = colormap[2::2]
        # Example: simplified_cmap[0] is [0.0666..., '#7a0402'], meaning values <= 0.0666... get '#7a0402'

        # 2. Normalize the values
        min_val = min(values)
        max_val = max(values)
        val_range = max_val - min_val

        # 3. Map values to colors
        mapped_colors = {}

        # Handle the edge case where all values are the same
        if val_range == 0:
            # Assign a default color (e.g., the color for the normalized value 0.5)
            default_color = None
            for threshold, color in simplified_cmap:
                if 0.5 <= threshold:
                    default_color = color
                    break
            if default_color is None: # Fallback if map doesn't explicitly cover 0.5 up to 1.0
                default_color = simplified_cmap[-1][1]
            for v in values:
                mapped_colors[v] = default_color
        else:
            for v in values:
                # Normalize the value to the [0, 1] range
                norm_v = (v - min_val) / val_range
                norm_v = max(0.0, min(1.0, norm_v))

                # Find the corresponding color from the simplified colormap
                assigned_color = None
                for threshold, color in simplified_cmap:
                    if norm_v <= threshold:
                        assigned_color = color
                        break

                if assigned_color is None:
                    assigned_color = simplified_cmap[-1][1]

                mapped_colors[v] = assigned_color


        # For clearer representation:
        for value, color in mapped_colors.items():
            norm_val_display = (value - min_val) / val_range if val_range != 0 else 0.5
            print(f"{value}: '{color}'")


        return mapped_colors  

