import os
from pyinstrument.session import Session

def test_shorten_path_equal_depth_prefers_first():

    #testing mutant 13

    s = Session(
        frame_records=[],          
        start_time=0.0,
        duration=0.0,
        min_interval=0.0,
        max_interval=0.0,
        sample_count=0,
        start_call_stack=[],
        target_description="test",
        cpu_time=0.0,
        sys_path=[],               
        sys_prefixes=[],           
    )

    joker = "fakest/path/ever.py" 

    s._short_file_path_cache.clear()

    
    candidate1 = os.path.join(joker, "file.py")
    candidate2 = os.path.join("src", "file.py")

    result1 = s.shorten_path(candidate1)
    result2 = s.shorten_path(candidate2)

    assert result2 == result1
  

