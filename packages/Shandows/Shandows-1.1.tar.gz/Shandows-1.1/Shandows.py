import os
import json5
import click
import shutil

from pathlib import Path
from dataclasses import dataclass


@dataclass
class Shandows:
	confFiPa: Path
	conf: dict
	homeDiPa: Path
	userName: str
	shadowDiPa: Path

	@staticmethod
	def isReal(pa: Path, isDir: bool):
		ans = pa.is_dir() if isDir else pa.is_file()
		ans = ans and not pa.is_symlink()
		return ans
		pass

	@staticmethod
	def delete(pa: Path, isDir: bool):
		if isDir:
			shutil.rmtree(pa)
			pass
		else:
			pa.unlink()
			pass
		pass

	def linkPath(self, origPa: Path, destPa: Path, isDir: bool):
		print("\n\t%s\n\t%s\n\t%s" % (isDir, origPa, destPa))

		if self.isReal(origPa, isDir):
			if destPa.exists():
				self.delete(origPa, isDir)
				pass
			else:
				shutil.move(origPa, destPa)
				pass
			origPa.symlink_to(destPa, isDir)
			pass
		else:
			if isDir:
				destPa.mkdir(parents=True, exist_ok=True)
				pass
			origPa.unlink(True)
			origPa.symlink_to(destPa, isDir)
		pass

	def linkApp(self, appTitle: str, jobs: dict):
		print('\n\n\n[%s]' % appTitle)
		appDiPa: Path = self.shadowDiPa / ('$' + appTitle)
		appDiPa.mkdir(exist_ok=True)

		for pa, isDir in jobs.items():
			origPa = self.homeDiPa / pa
			destPa = appDiPa / pa
			self.linkPath(origPa, destPa, isDir)
			pass
		pass

	def run(self):
		for appTitle, jobs in self.conf.items():
			self.linkApp(appTitle, jobs)
			pass
		pass

	pass


@click.command()
@click.option(
	'-c', '--confFiPa', 'confFiPa', metavar='',
	required=True, help='Json5 config file path.',
	type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
)
def CLI(confFiPa: Path):
	conf: dict = json5.loads(confFiPa.read_text('u8'))
	homeDiPa: Path = Path(os.environ['UserProfile']).absolute()
	userName: str = homeDiPa.name
	shadowDiPa = confFiPa.parent / ('%' + userName)

	shandows = Shandows(confFiPa, conf, homeDiPa, userName, shadowDiPa)
	shandows.run()
	pass


if __name__ == '__main__':
	CLI()
	pass
