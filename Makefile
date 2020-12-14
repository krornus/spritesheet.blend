ZIP := zip

ADDON := spritesheet

SOURCES := $(wildcard $(ADDON)/*.py)

ZIPFILE := $(ADDON).zip
ZIPFLAGS := -qu

PYTHON := "$(BLENDER_PYTHON_PATH)/bin/python.exe"

.PHONY: zip
zip: $(ZIPFILE)

.PHONY: install
install:
	cp -r "$(ADDON)" "$(ADDONS)"

.PHONY: check-install
check-install:
ifndef ADDONS
    $(error $$ADDONS directory not set)
endif
	

.PHONY: clean
clean:
	$(RM) $(ZIPFILE)

$(ZIPFILE): $(SOURCES)
	$(ZIP) $(ZIPFLAGS) $@ $?
