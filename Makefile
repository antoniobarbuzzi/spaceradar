PHONY: clean

clean:
	python setup.py clean --all
	rm -rf build dist *.egg-info *deb reports
	find . -name "*.pyc" -delete
