import numpy as np
import os
import hashlib
import pickle
from modules.atmosphere_f import atmosphere_m

class FastAtmosphere:
    def __init__(self, max_alt=85000.0, step=10.0, cache_dir="cache"):
        self.max_alt = max_alt
        self.step = step
        self.cache_path = os.path.join(cache_dir, "atm_cache.pkl")
        
        # 1. Generate a checksum of the logic source file
        current_logic_hash = self._get_source_hash("modules/atmosphere_f.py")
        
        # 2. Try to load existing cache
        if self._load_cache(current_logic_hash):
            return # Successfully loaded valid cache
            
        # 3. Otherwise, generate and save
        print(f"Atmosphere cache invalid or missing. Regenerating to {max_alt}m...")
        self._generate_table()
        self._save_cache(current_logic_hash)

    def _get_source_hash(self, filepath):
        """Creates a unique MD5 hash based on the content of the logic file."""
        if not os.path.exists(filepath):
            return "default"
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def _generate_table(self):
        """The original generation logic."""
        self.altitudes = np.arange(0, self.max_alt + self.step, self.step)
        self.densities = np.zeros_like(self.altitudes)
        self.pressures = np.zeros_like(self.altitudes)
        self.temps = np.zeros_like(self.altitudes)
        self.viscosities = np.zeros_like(self.altitudes)
        
        for i, alt in enumerate(self.altitudes):
            atm = atmosphere_m(alt, geometric=True)
            self.densities[i] = atm["rho_kgm3"]
            self.pressures[i] = atm["p_Pa"]
            self.temps[i] = atm["T_K"]
            self.viscosities[i] = atm["mu_Pas"]

    def _save_cache(self, logic_hash):
        """Saves data and the current hash to a pickle file."""
        if not os.path.exists(os.path.dirname(self.cache_path)):
            os.makedirs(os.path.dirname(self.cache_path))
            
        data = {
            "hash": logic_hash,
            "max_alt": self.max_alt,
            "step": self.step,
            "altitudes": self.altitudes,
            "densities": self.densities,
            "pressures": self.pressures,
            "temps": self.temps,
            "viscosities": self.viscosities
        }
        with open(self.cache_path, "wb") as f:
            pickle.dump(data, f)

    def _load_cache(self, current_logic_hash):
        """Loads cache if it exists and the hash/parameters match."""
        if not os.path.exists(self.cache_path):
            return False
            
        try:
            with open(self.cache_path, "rb") as f:
                data = pickle.load(f)
            
            # Check if logic, max altitude, or step size changed
            if (data["hash"] == current_logic_hash and 
                data["max_alt"] == self.max_alt and 
                data["step"] == self.step):
                
                self.altitudes = data["altitudes"]
                self.densities = data["densities"]
                self.pressures = data["pressures"]
                self.temps = data["temps"]
                self.viscosities = data["viscosities"]
                return True
        except Exception:
            return False # Fallback to regeneration if file is corrupt
        return False

    def get_atm(self, alt_m: float) -> dict:
        """Fetch interpolated atmospheric properties at high speed."""
        return {
            "rho_kgm3": np.interp(alt_m, self.altitudes, self.densities),
            "p_Pa": np.interp(alt_m, self.altitudes, self.pressures),
            "T_K": np.interp(alt_m, self.altitudes, self.temps),
            "mu_Pas": np.interp(alt_m, self.altitudes, self.viscosities)
        }