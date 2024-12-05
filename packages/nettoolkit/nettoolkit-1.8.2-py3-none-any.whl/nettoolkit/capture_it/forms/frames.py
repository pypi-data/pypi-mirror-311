
from nettoolkit.nettoolkit.forms.formitems import *

# ===================================================================

def capture_it_frame():
	"""tab display - Credential inputs

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	cumulative=('cumulative', 'non-cumulative', 'both')
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[


		[sg.Text('Credentials',  font=('TimesNewRoman', 12), text_color="black"),], 
		[sg.Text("un:",     text_color="black"),sg.InputText(get_cache(CACHE_FILE, 'cit_cred_un'), key='cit_cred_un', size=(8,1), change_submits=True),
		 sg.Text("pw:",     text_color="black"),sg.InputText("", key='cit_cred_pw', password_char='*', size=(20,1),),
		 sg.Text("secret:", text_color="black"),sg.InputText("", key='cit_cred_en',  password_char='*', size=(20,1)), ],
		under_line(80),

		[sg.Text('output folder:\t\t', text_color="black"), 
		 sg.InputText(get_cache(CACHE_FILE, 'cit_path_captures'), key='cit_path_captures', change_submits=True),  
		 sg.FolderBrowse(button_color="orange"), 
		 sg.Button("open", change_submits=True, key='cit_folder_path_captures_open', button_color="darkgrey"),],
		[sg.Text('execution log folder:\t', text_color="black"), 
		 sg.InputText(get_cache(CACHE_FILE, 'cit_path_logs'), key='cit_path_logs', change_submits=True), 
		 sg.FolderBrowse(button_color="orange"), 
		 sg.Button("open", change_submits=True, key='cit_folder_path_logs_open', button_color="darkgrey"),],
		[sg.Text('summary log folder:\t', text_color="black"), 
		 sg.InputText(get_cache(CACHE_FILE, 'cit_path_summary'), key='cit_path_summary', change_submits=True),  
		 sg.FolderBrowse(button_color="orange"), 
		 sg.Button("open", change_submits=True, key='cit_folder_path_summary_open', button_color="darkgrey"),],

		[sg.Text('Hosts/IPs file:\t\t', text_color="black"), 
	     sg.InputText(get_cache(CACHE_FILE, 'cit_file_hosts'), size=(30,1),  key='cit_file_hosts', change_submits=True,), 
	     sg.FileBrowse(button_color="grey"), sg.Button("open file", change_submits=True, key='cit_file_hosts_open', button_color="darkgrey"),],
		[sg.Text('Cisco commands file:\t', text_color="black"), 
	     sg.InputText(get_cache(CACHE_FILE, 'cit_file_cisco'), size=(30,1), key='cit_file_cisco', change_submits=True,), 
	     sg.FileBrowse(button_color="grey"), sg.Button("open file", change_submits=True, key='cit_file_cisco_open', button_color="darkgrey"),],
		[sg.Text('Juniper Commands file:\t', text_color="black"), 
	     sg.InputText(get_cache(CACHE_FILE, 'cit_file_juniper'), size=(30,1), key='cit_file_juniper', change_submits=True,), 
	     sg.FileBrowse(button_color="grey"), sg.Button("open file", change_submits=True, key='cit_file_juniper_open', button_color="darkgrey"),],
		[sg.Text('Custom Package Yaml file:\t', text_color="black"), 
	     sg.InputText(get_cache(CACHE_FILE, 'cit_file_custom_yml'), key='cit_file_custom_yml', change_submits=True,), 
	     sg.FileBrowse(button_color="grey"), ],
		under_line(80),

		[sg.Checkbox('capture only missing outputs (appends)\t',	key='cit_opt_missing',       default=False, text_color='black'),
		 sg.Checkbox('capture append mode',							key='cit_opt_append',        default=False, text_color='black'),],
		[sg.Checkbox('custom commands\t\t\t\t',						key='cit_opt_dependent',     default=True,  text_color='black'),
		 sg.Checkbox('Excel parsed file',       	       			key='cit_opt_parsed_output', default=False, text_color='black'), ],
		[sg.Checkbox('Transpose summary log\t\t\t',   	    		key='cit_opt_summary_xpose', default=True,  text_color='black'),
		 sg.Checkbox('Forced Login',                    			key='cit_opt_forced_login',  default=True,  text_color='black')],
		[sg.Text('Output Mode:', text_color="black"), 
		 sg.InputCombo(cumulative, default_value=cumulative[0], key='cit_opt_cumulative', size=(15,1)),],
		[sg.Text('Concurrent Connections ', text_color="black"), 
		 sg.InputText(100,  key='cit_opt_max_connections', size=(5,1) ), sg.Text('Use 1 for sequential process', text_color="white"), ],


		[sg.Text('\t\t\t\t\t\t\t\t'),
		 sg.Button("Capture-it", change_submits=True, size=(20,1), key='cit_btn_start', button_color="blue"),],

		])



def capture_it_by_xl_frame():
	"""tab display - Credential inputs

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	cumulative=('cumulative', 'non-cumulative', 'both')
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Credentials',  font=('TimesNewRoman', 12), text_color="black"),], 
		[sg.Text("un:",     text_color="black"),sg.InputText(get_cache(CACHE_FILE, 'cit_cred_un'), key='cit_cred_un1', size=(8,1), change_submits=True),
		 sg.Text("pw:",     text_color="black"),sg.InputText("", key='cit_cred_pw1', password_char='*', size=(20,1),),
		 sg.Text("secret:", text_color="black"),sg.InputText("", key='cit_cred_en1',  password_char='*', size=(20,1)), ],
		under_line(80),

		[sg.Text('output folder:\t\t', text_color="black"), 
		 sg.InputText(get_cache(CACHE_FILE, 'cit_path_captures'), key='cit_path_captures1', change_submits=True),  
		 sg.FolderBrowse(button_color="orange"), 
		 sg.Button("open", change_submits=True, key='cit_folder_path_captures_open1', button_color="darkgrey"),],
		[sg.Text('execution log folder:\t', text_color="black"), 
		 sg.InputText(get_cache(CACHE_FILE, 'cit_path_logs'), key='cit_path_logs1', change_submits=True), 
		 sg.FolderBrowse(button_color="orange"), 
		 sg.Button("open", change_submits=True, key='cit_folder_path_logs_open1', button_color="darkgrey"),],
		[sg.Text('summary log folder:\t', text_color="black"), 
		 sg.InputText(get_cache(CACHE_FILE, 'cit_path_summary'), key='cit_path_summary1', change_submits=True),  
		 sg.FolderBrowse(button_color="orange"), 
		 sg.Button("open", change_submits=True, key='cit_folder_path_summary_open1', button_color="darkgrey"),],

		[sg.Text('Device-Commands Excel file:', text_color="black"), 
	     sg.InputText(get_cache(CACHE_FILE, 'cit_by_xl_file_dev_cmd_xl_file'), size=(30,1),  key='cit_by_xl_file_dev_cmd_xl_file', change_submits=True,), 
	     sg.FileBrowse(button_color="grey"), sg.Button("open file", change_submits=True, key='cit_by_xl_file_dev_cmd_xl_file_open', button_color="darkgrey"),],
		blank_line(),
		blank_line(),

		[sg.Text('Custom Package Yaml file:\t', text_color="black"), 
	     sg.InputText(get_cache(CACHE_FILE, 'cit_file_custom_yml'), key='cit_file_custom_yml1', change_submits=True,), 
	     sg.FileBrowse(button_color="grey"), ],
		under_line(80),

		[sg.Checkbox('capture only missing outputs (appends)\t',key='cit_opt_missing1',       default=False, text_color='black'),
		 sg.Checkbox('capture append mode',						key='cit_opt_append1',        default=False, text_color='black', disabled=True), ],
		[sg.Checkbox('custom commands\t\t\t\t', 				key='cit_opt_dependent1',     default=True,  text_color='black'),
		 sg.Checkbox('Excel parsed file',						key='cit_opt_parsed_output1', default=False, text_color='black', disabled=True), ],
		[sg.Checkbox('Transpose summary log\t\t\t',				key='cit_opt_summary_xpose1', default=True,  text_color='black'),
		 sg.Checkbox('Forced Login',							key='cit_opt_forced_login1',  default=True,  text_color='black')],
		[sg.Text('Output Mode:', text_color="black"), 
		 sg.InputCombo(cumulative, default_value=cumulative[0], key='cit_opt_cumulative1', size=(15,1)),],
		[sg.Text('Concurrent Connections ', text_color="black"), 
		 sg.InputText(100,  key='cit_opt_max_connections1', size=(5,1) ), sg.Text('Use 1 for sequential process', text_color="white"), ],


		[sg.Text('\t\t\t\t\t\t\t\t'),
		 sg.Button("Capture-it using Excel", change_submits=True, size=(20,1), key='cit_by_xl_btn_start', button_color="blue"),],

		])




CAPTUREIT_FRAMES = {
	'Capture-It': capture_it_frame(),
	'Capture-It using-Excel': capture_it_by_xl_frame(),
}