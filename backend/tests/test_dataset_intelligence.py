from app.services.dataset_intelligence import analyze_dataset


CSV_DATA = b"""age,city,income,target
20,Lahore,50000,no
22,Lahore,60000,no
25,Islamabad,80000,yes
30,Karachi,90000,yes
"""


def test_analyze_dataset():
    result = analyze_dataset(CSV_DATA)

    assert "dataset" in result
    assert "columns" in result
    assert "quality" in result
    assert "task" in result
    assert "ydata_profile" in result

    assert result["dataset"]["rows"] == 4
    assert result["dataset"]["columns"] == 4

    assert result["task"]["target_column"] == "target"
    assert result["task"]["task_type"] == "classification"

    assert len(result["columns"]["info"]) == 4
    assert "age" in result["columns"]["types"]["numeric"]
    assert "city" in result["columns"]["types"]["categorical"]

    assert "validation" in result
    assert result["validation"]["success"] is True
    assert len(result["validation"]["expectations"]) == 4