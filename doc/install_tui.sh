#!/bin/bash

yum -y install newt dialog
yum -y install bash

gui_install_or_update ()
{
	OPTION=$(whiptail --title "Install OR Update" --menu "###\n# Welcome,\n# You now have to choose between install or update an InMan component\n###" 25 78 10 \
	"Install" "Install new component" \
	"Update" "Update an existing component" 3>&1 1>&2 2>&3)

	exitstatus=$?
	if [ $exitstatus = 0 ]; then
		echo $OPTION
	else
		echo "Cancel"
	fi
}

gui_install_choice ()
{
	OPTION=$(whiptail --title "Install choice" --checklist \
	"Choose which part to install" 25 78 4 \
	"Radius server" "Install Radius service" OFF \
	"InMan Radius Agent" "Install Agent for InMan management" OFF \
	"InMan Radius Cluster plugin" "Plugin Master/Slave Radius management" OFF \
	"InMan server" "Install WebUI and master engine" OFF 3>&1 1>&2 2>&3)

	exitstatus=$?
	if [ $exitstatus = 0 ]; then
		echo $OPTION
	else
		echo "Cancel"
	fi
}

RET_INSTALL_UPDATE_CHOICE=$(gui_install_or_update)
RET_INSTALL_OPTION_CHOICE=""
RET_UPDATE_OPTION_CHOICE=""

if [ $RET_INSTALL_UPDATE_CHOICE = "Install" ]; then
	echo $RET_INSTALL_UPDATE_CHOICE
	RET_INSTALL_OPTION_CHOICE=$(gui_install_choice)
elif [ $RET_INSTALL_UPDATE_CHOICE = "Update" ]; then
	echo $RET_INSTALL_UPDATE_CHOICE
else
	echo "Cancel."
fi

if [ -n "$RET_INSTALL_OPTION_CHOICE" ]; then
	IFS='"' read -ra D_INSTALL_OPTIONS <<< "$RET_INSTALL_OPTION_CHOICE"    #Convert string to array

	echo "$RET_INSTALL_OPTION_CHOICE"

	#Print all names from array
	for i in "${D_INSTALL_OPTIONS[@]}"; do
		INSTALL_FILE_NAME=install_$(echo "$i" | sed -E -e 's/[[:blank:]]+/_/g').sh
		###
		### Faire la verification de savoir si on install le plugin master/slave en envoyant 
		### la liste de ce qui va etre installer. Les installeur etant libre de lire ou non la liste
		### et appliquer alors une regle ou pas
		###
		if [ -e $INSTALL_FILE_NAME ]; then
			bash $INSTALL_FILE_NAME "$RET_INSTALL_OPTION_CHOICE"
		fi
	done
elif [ -n "$RET_UPDATE_OPTION_CHOICE" ]; then
	echo "Update"
else
	echo "Cancel."
fi

#####
# Test to get dynamically update option like different version available to update a program
#####

#	UPDATE_OPTION="\"Radius server\" \"Install Radius service\" OFF \
#		\"InMan Radius Agent\" \"Install Agent for InMan management\" OFF \
#		\"InMan Radius Cluster plugin\" \"Plugin Master/Slave Radius management\" OFF \
#		\"InMan server\" \"Install WebUI and master engine\" OFF"

#eval "whiptail --title \"Install choice\" --checklist \
#\"Choose which part to install\" 25 78 4 \
#$UPDATE_OPTION \
# 3>&1 1>&2 2>&3"