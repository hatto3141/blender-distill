import bpy
import os
import sys
from datetime import datetime
from typing import TextIO, List, Optional

def get_target_info(var: bpy.types.DriverVariable) -> str:
    """Resolves driver variable targets to a readable string."""
    targets = []
    for target in var.targets:
        t_id = target.id.name if target.id else "None"
        t_bone = f"Bone['{target.bone_target}']" if target.bone_target else ""
        t_path = f"Path['{target.data_path}']" if target.data_path else ""
        
        # Construct concise reference string
        ref_parts = [p for p in [t_id, t_bone, t_path] if p]
        targets.append(" -> ".join(ref_parts) if ref_parts else "Unknown Ref")
    
    return ", ".join(targets)

def write_driver_data(f: TextIO, drivers: bpy.types.AnimDataDrivers) -> None:
    """Writes driver details to the log buffer."""
    for d in drivers:
        target_prop = d.data_path
        if d.array_index >= 0:
            target_prop += f"[{d.array_index}]"
            
        f.write(f"  [Target]: {target_prop}\n")
        f.write(f"    Expr: {d.driver.expression}\n")
        
        if d.driver.variables:
            f.write("    Vars:\n")
            for var in d.driver.variables:
                ref_info = get_target_info(var)
                f.write(f"      - {var.name}: {ref_info}\n")
        f.write("\n")

def analyze_drivers(output_path: str) -> None:
    """Main analysis routine for scene drivers."""
    start_time = datetime.now()
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"=== Driver Analysis Report ===\n")
            f.write(f"Generated: {start_time}\n")
            f.write(f"File: {bpy.data.filepath}\n")
            f.write("="*40 + "\n\n")

            # 1. Iterate over all objects in the blend file
            # Using bpy.data.objects ensures we catch hidden/disabled objects too
            for obj in bpy.data.objects:
                has_obj_drivers = obj.animation_data and obj.animation_data.drivers
                has_data_drivers = (obj.type == 'ARMATURE' and obj.data.animation_data 
                                    and obj.data.animation_data.drivers)

                if not (has_obj_drivers or has_data_drivers):
                    continue

                f.write(f"OBJECT: {obj.name} ({obj.type})\n")
                f.write("-" * 30 + "\n")

                if has_obj_drivers:
                    f.write("  <Object Level Drivers>\n")
                    write_driver_data(f, obj.animation_data.drivers)

                if has_data_drivers:
                    f.write("  <Armature Data Drivers>\n")
                    write_driver_data(f, obj.data.animation_data.drivers)
                
                f.write("-" * 30 + "\n\n")

        print(f"SUCCESS: Report saved to {output_path}")

    except IOError as e:
        print(f"ERROR: File write failed - {e}", file=sys.stderr)
    except Exception as e:
        print(f"ERROR: Unexpected failure - {e}", file=sys.stderr)

if __name__ == "__main__":
    # Ensure standard output location if not specified
    log_path = os.path.expanduser("~/driver_analysis_log.txt")
    analyze_drivers(log_path)
